#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""What the registrar needs, and the comparison with what the parent publishes (DESIGN 7.2)."""
import json
import os
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'imageroot', 'pypkg'))

from pdnsmodule import core, dnsutil

DS = '12345 13 2 ABCDEF0123'


def servers(*entries):
    return [{'ns_name': n, 'glue': g, 'addresses': [{'address': a, 'public': dnsutil.is_public(a)} for a in addrs]}
            for n, g, addrs in entries]


def observed(names, glue=None):
    return {'parent': 'com.', 'server': 'a.gtld-servers.net.', 'nxdomain': not names,
            'name_servers': sorted(dnsutil.canonical(n) for n in names),
            'glue': {dnsutil.canonical(k): v for k, v in (glue or {}).items()}}


class NameServers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
        json.dump({'peers': [
            {'kind': 'internal', 'ns_name': 'ns2.example.net', 'advertise': True, 'addresses': ['2606:4700:4700::1001']},
            {'kind': 'internal', 'ns_name': 'hidden.example.net', 'advertise': False, 'addresses': ['192.0.2.3']},
        ]}, self.tmp)
        self.tmp.close()
        self.settings = core.Settings('powerdns1', 'ns1.example.com', addresses=['192.168.1.5', '1.1.1.1'],
                                      peers_file=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_lists_advertised_servers_with_glue_and_public_flags(self):
        out = core.name_servers(self.settings, 'example.com')
        self.assertEqual([n['ns_name'] for n in out], ['ns1.example.com', 'ns2.example.net'])
        ns1, ns2 = out
        self.assertTrue(ns1['glue'])
        self.assertFalse(ns2['glue'])
        self.assertEqual(ns1['addresses'], [{'address': '192.168.1.5', 'public': False},
                                            {'address': '1.1.1.1', 'public': True}])

    def test_glue_warnings_still_names_in_zone_servers(self):
        self.assertEqual(core.glue_warnings(self.settings, 'example.net'),
                         [{'ns_name': 'ns2.example.net', 'addresses': ['2606:4700:4700::1001']}])


class Compare(unittest.TestCase):
    NS = servers(('ns1.example.com', True, ['1.1.1.1', '2606:4700:4700::1111']), ('ns2.example.net', False, []))

    def compare(self, seen, ds_expected=(), ds_published=(), resolution='ok'):
        return core.compare_delegation('example.com', self.NS, list(ds_expected), seen,
                                       None if ds_published is None else list(ds_published), resolution)

    def test_everything_in_place(self):
        out = self.compare(observed(['ns1.example.com', 'ns2.example.net'],
                                    {'ns1.example.com': ['2606:4700:4700:0::1111', '1.1.1.1']}), [DS], [DS])
        self.assertTrue(out['delegated'])
        self.assertEqual((out['ns_missing'], out['ns_extra']), ([], []))
        self.assertEqual(out['glue'], [{'ns_name': 'ns1.example.com', 'expected': ['1.1.1.1', '2606:4700:4700::1111'],
                                        'published': ['1.1.1.1', '2606:4700:4700:0::1111'], 'ok': True}])
        self.assertTrue(out['ds_ok'])
        self.assertEqual(out['parent'], 'com')

    def test_old_provider_still_listed(self):
        out = self.compare(observed(['ns1.example.com', 'ns.oldhost.example']))
        self.assertEqual(out['ns_missing'], ['ns2.example.net'])
        self.assertEqual(out['ns_extra'], ['ns.oldhost.example'])
        self.assertFalse(out['glue'][0]['ok'])

    def test_not_delegated(self):
        out = self.compare(observed([]), resolution='nxdomain')
        self.assertFalse(out['delegated'])
        self.assertEqual(out['ns_missing'], ['ns1.example.com', 'ns2.example.net'])

    def test_no_parent_answer(self):
        out = self.compare(None, ds_published=None, resolution=None)
        self.assertIsNone(out['delegated'])
        self.assertIsNone(out['ns_published'])
        self.assertEqual(out['glue'], [])
        self.assertIsNone(out['ds_ok'])

    def test_signed_zone_without_ds_is_not_ok(self):
        self.assertFalse(self.compare(observed(['ns1.example.com']), [DS], [])['ds_ok'])

    def test_stale_ds_breaks_validation(self):
        out = self.compare(observed(['ns1.example.com']), [DS], [DS, '999 8 2 00FF'], resolution='servfail')
        self.assertFalse(out['ds_ok'])

    def test_unsigned_zone_must_have_no_ds(self):
        self.assertTrue(self.compare(observed(['ns1.example.com']), [], [])['ds_ok'])
        self.assertFalse(self.compare(observed(['ns1.example.com']), [], [DS])['ds_ok'])

    def test_other_digest_types_match_on_key_tag(self):
        self.assertTrue(self.compare(observed(['ns1.example.com']), [DS], ['12345 13 4 AA' * 3])['ds_ok'])


class Wire(unittest.TestCase):
    def test_read_name_follows_compression(self):
        buf = b'\0' * 12 + b'\x07example\x03com\x00' + b'\x03ns1\xc0\x0c'
        self.assertEqual(dnsutil.read_name(buf, 12), 'example.com.')
        self.assertEqual(dnsutil.read_name(buf, 25), 'ns1.example.com.')

    def test_read_name_refuses_a_loop(self):
        with self.assertRaises(ValueError):
            dnsutil.read_name(b'\xc0\x00', 0)

    def test_records_reads_owner_and_type(self):
        rr = b'\x03www\x00' + struct.pack('!HHIH', 1, 1, 60, 4) + bytes([192, 0, 2, 1])
        records, pos = dnsutil._records(rr, 0, 1)
        self.assertEqual(records[0][:3], ('www.', 1, bytes([192, 0, 2, 1])))
        self.assertEqual(pos, len(rr))

    def test_is_public(self):
        self.assertTrue(dnsutil.is_public('2605:a140:2212:2763::1'))
        for private in ('10.5.4.1', '192.168.1.5', 'fd00::1', 'not an address'):
            self.assertFalse(dnsutil.is_public(private), private)


if __name__ == '__main__':
    unittest.main()
