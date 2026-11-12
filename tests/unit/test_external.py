#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""External secondaries: the rules for a peer record, and the NS records it adds (DESIGN 6.6)."""
import base64
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'imageroot', 'pypkg'))

from pdnsmodule import core

ZONES = {'example.com.', 'example.org.'}


def normalize(request, peers=(), peer_id=None):
    return core.normalize_external(request, list(peers), ZONES, peer_id=peer_id)


class Normalize(unittest.TestCase):
    def assertRefused(self, code, request, peers=()):
        with self.assertRaises(core.ActionError) as cm:
            normalize(request, peers)
        self.assertEqual(cm.exception.code, code)

    def test_defaults(self):
        peer = normalize({'name': 'Provider', 'notify': ['203.0.113.53']})
        self.assertEqual(peer, {'id': 'ext1', 'kind': 'external', 'name': 'Provider', 'notify': ['203.0.113.53'],
                                'auth': 'tsig', 'transfer_from': [], 'ns_names': [], 'advertise': True,
                                'zones': 'all'})

    def test_ids_fill_gaps_and_are_never_shared(self):
        peers = [{'kind': 'external', 'id': 'ext1', 'name': 'a'}, {'kind': 'external', 'id': 'ext3', 'name': 'c'},
                 {'kind': 'internal', 'id': 'powerdns2'}]
        self.assertEqual(normalize({'name': 'b', 'notify': ['192.0.2.1']}, peers)['id'], 'ext2')

    def test_names_are_unique_ignoring_case(self):
        peers = [{'kind': 'external', 'id': 'ext1', 'name': 'Provider'}]
        self.assertRefused('name_exists', {'name': 'provider', 'notify': ['192.0.2.1']}, peers)
        # but a peer keeps its own name on update
        self.assertEqual(normalize({'name': 'Provider', 'notify': ['192.0.2.1']}, peers, 'ext1')['id'], 'ext1')

    def test_notify_addresses(self):
        self.assertRefused('notify_required', {'name': 'p', 'notify': [' ']})
        self.assertRefused('invalid_address', {'name': 'p', 'notify': ['ns1.example.net']})
        peer = normalize({'name': 'p', 'notify': ['2001:DB8::1', '192.0.2.1', '192.0.2.1']})
        self.assertEqual(peer['notify'], ['2001:db8::1', '192.0.2.1'])

    def test_ip_only_needs_narrow_networks(self):
        self.assertRefused('transfer_from_required', {'name': 'p', 'notify': ['192.0.2.1'], 'auth': 'ip'})
        self.assertRefused('network_too_wide', {'name': 'p', 'notify': ['192.0.2.1'], 'auth': 'ip',
                                                'transfer_from': ['198.51.0.0/16']})
        self.assertRefused('network_too_wide', {'name': 'p', 'notify': ['192.0.2.1'], 'auth': 'ip',
                                                'transfer_from': ['0.0.0.0/0']})
        self.assertRefused('network_too_wide', {'name': 'p', 'notify': ['192.0.2.1'], 'auth': 'ip',
                                                'transfer_from': ['2001:db8::/32']})
        self.assertRefused('invalid_network', {'name': 'p', 'notify': ['192.0.2.1'], 'auth': 'ip',
                                               'transfer_from': ['slave.example.net']})
        peer = normalize({'name': 'p', 'notify': ['192.0.2.1'], 'auth': 'ip',
                          'transfer_from': ['198.51.100.7', '198.51.100.9/24', '2001:db8:1::/48']})
        self.assertEqual(peer['transfer_from'], ['198.51.100.7/32', '198.51.100.0/24', '2001:db8:1::/48'])

    def test_tsig_peer_keeps_no_networks(self):
        peer = normalize({'name': 'p', 'notify': ['192.0.2.1'], 'transfer_from': ['198.51.100.7']})
        self.assertEqual(peer['transfer_from'], [])

    def test_ns_names_and_zones(self):
        self.assertRefused('invalid_ns_name', {'name': 'p', 'notify': ['192.0.2.1'], 'ns_names': ['bad name']})
        self.assertRefused('zone_not_found', {'name': 'p', 'notify': ['192.0.2.1'], 'zones': ['example.net']})
        peer = normalize({'name': 'p', 'notify': ['192.0.2.1'], 'ns_names': ['NS1.Provider.example.'],
                          'zones': ['example.org.', 'example.com', 'Example.com']})
        self.assertEqual(peer['ns_names'], ['ns1.provider.example'])
        self.assertEqual(peer['zones'], ['example.com', 'example.org'])


class Tsig(unittest.TestCase):
    def test_generated_secrets_match_the_digest_size(self):
        for algorithm, size in core.TSIG_ALGORITHMS.items():
            self.assertEqual(len(base64.b64decode(core.generate_tsig_secret(algorithm))), size)

    def test_request(self):
        self.assertEqual(core._tsig_request({}), ('hmac-sha256', '', ''))
        self.assertEqual(core._tsig_request({'tsig': {'key_name': 'transfer-key'}}), ('hmac-sha256', 'transfer-key', ''))
        self.assertEqual(core._tsig_request({'tsig': {'algorithm': 'hmac-sha512', 'key_name': 'k.example.',
                                                      'secret': 'c2VjcmV0'}}),
                         ('hmac-sha512', 'k.example', 'c2VjcmV0'))
        for tsig, code in (({'algorithm': 'hmac-sha3'}, 'invalid_tsig_algorithm'),
                           ({'key_name': 'two words'}, 'invalid_tsig_key_name'),
                           ({'secret': 'not base64!'}, 'invalid_tsig_secret')):
            with self.assertRaises(core.ActionError) as cm:
                core._tsig_request({'tsig': tsig})
            self.assertEqual(cm.exception.code, code)


class NsNames(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
        json.dump({'peers': [
            {'kind': 'internal', 'ns_name': 'ns2.example.net', 'advertise': True},
            {'kind': 'external', 'id': 'ext1', 'ns_names': ['ns1.provider.example', 'ns2.provider.example'],
             'advertise': True, 'zones': ['example.com']},
            {'kind': 'external', 'id': 'ext2', 'ns_names': ['ns.hidden.example'], 'advertise': False, 'zones': 'all'},
            {'kind': 'external', 'id': 'ext3', 'ns_names': ['ns.all.example'], 'advertise': True, 'zones': 'all'},
        ]}, self.tmp)
        self.tmp.close()
        self.settings = core.Settings('powerdns1', 'ns1.example.com', peers_file=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_external_names_only_on_the_zones_given(self):
        self.assertEqual(core.ns_names(self.settings, 'example.com'),
                         ['ns.all.example.', 'ns1.example.com.', 'ns1.provider.example.', 'ns2.example.net.',
                          'ns2.provider.example.'])
        self.assertEqual(core.ns_names(self.settings, 'example.org.'),
                         ['ns.all.example.', 'ns1.example.com.', 'ns2.example.net.'])

    def test_external_names_are_reported_without_addresses(self):
        out = {n['ns_name']: n for n in core.name_servers(self.settings, 'provider.example')}
        self.assertEqual(out['ns.all.example']['addresses'], [])
        self.assertFalse(out['ns.all.example']['glue'])


if __name__ == '__main__':
    unittest.main()
