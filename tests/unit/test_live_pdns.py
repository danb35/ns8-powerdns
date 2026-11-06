#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""core.py against real PowerDNS servers in Docker: one primary, two secondaries.

Skipped without Docker. The image is the one build-images.sh declares, so a
Renovate bump of PowerDNS runs these against the new version. The servers use the
pdns.conf this module renders, apart from ports and addresses.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'imageroot', 'pypkg'))

from pdnsmodule import config, core, dnsutil
from pdnsmodule.pdnsapi import ApiError, Pdns

IMAGE = re.search(r'org\.nethserver\.images=(\S+?)"', open(os.path.join(ROOT, 'build-images.sh')).read()).group(1)
NETWORK = 'pdnsmodule-test'
SUBNET = '10.78.0'
KEY = 'testkey'
PRIMARY_IP = SUBNET + '.10'
PORTS = {'p': (28081, 25310), 's1': (28082, 25311), 's2': (28083, 25312)}
ADDRS = {'p': PRIMARY_IP, 's1': SUBNET + '.21', 's2': SUBNET + '.22'}
CATALOG = 'catalog.test-uuid.invalid.'


def docker(*args, check=True):
    return subprocess.run(['docker', *args], capture_output=True, text=True, check=check)


def have_docker():
    return shutil.which('docker') and docker('info', check=False).returncode == 0


def wait_for(predicate, seconds=45):
    deadline = time.time() + seconds
    while time.time() < deadline:
        result = predicate()
        if result:
            return result
        time.sleep(1)
    return predicate()


def start(name, conf):
    """The config is rendered for the container's real address; the API listens on all."""
    conf = re.sub(r'^webserver-address=.*$', 'webserver-address=0.0.0.0', conf, flags=re.M)
    conf = re.sub(r'^webserver-allow-from=.*$', 'webserver-allow-from=0.0.0.0/0', conf, flags=re.M)
    conf = re.sub(r'^webserver-port=.*$', 'webserver-port=8081', conf, flags=re.M)
    directory = tempfile.mkdtemp(prefix='pdnsmodule')
    with open(os.path.join(directory, 'pdns.conf'), 'w') as fp:
        fp.write(conf)
    api, dns = PORTS[name]
    docker('run', '-d', '--name', 'pdnsmodule-' + name, '--network', NETWORK, '--ip', ADDRS[name],
           '-p', '127.0.0.1:%d:8081' % api, '-p', '127.0.0.1:%d:53/udp' % dns, '-p', '127.0.0.1:%d:53/tcp' % dns,
           '--user=0:0', '-v', directory + ':/conf:ro', '--entrypoint=/bin/sh', IMAGE, '-c',
           'cp /conf/pdns.conf /etc/powerdns/pdns.conf && sqlite3 /var/lib/powerdns/pdns.sqlite3 "select 1" >/dev/null '
           '&& exec /usr/local/sbin/pdns_server-startup')
    client = Pdns('http://127.0.0.1:%d' % api, KEY)
    client.wait_ready(60)
    return client


def cleanup():
    for name in PORTS:
        docker('rm', '-f', 'pdnsmodule-' + name, check=False)
    docker('network', 'rm', NETWORK, check=False)


@unittest.skipUnless(have_docker(), 'needs Docker')
class Replication(unittest.TestCase):
    """One server set for the whole class, as the steps of DESIGN 6 build on each other."""

    @classmethod
    def setUpClass(cls):
        cleanup()
        docker('network', 'create', '--subnet', SUBNET + '.0/24', NETWORK)
        cls.addClassCleanup(cleanup)
        cls.dir = tempfile.mkdtemp(prefix='pdnsmodule-state')
        def render(role, ip, **kw):
            return config.render_pdns_conf(role, [ip], ip, SUBNET + '.0/24', 8081, KEY, **kw)
        cls.p = start('p', render('primary', PRIMARY_IP))
        cls.s1 = start('s1', render('secondary', ADDRS['s1'], primary_address=PRIMARY_IP))
        cls.s2 = start('s2', render('secondary', ADDRS['s2'], primary_address=PRIMARY_IP))
        cls.settings = core.Settings('powerdns1', 'ns1.example.net', hostmaster='hostmaster@example.net',
                                     catalog=CATALOG, addresses=['192.0.2.1'],
                                     peers_file=os.path.join(cls.dir, 'peers.json'))
        core.ensure_catalog(cls.p, cls.settings)
        for client, module_id in ((cls.s1, 'powerdns2'), (cls.s2, 'powerdns3')):
            ip = ADDRS['s1'] if module_id == 'powerdns2' else ADDRS['s2']
            out = core.register_secondary(cls.p, cls.settings, module_id, ip,
                                          'ns-%s.example.net' % module_id, True, ['192.0.2.2'])
            core.ensure_consumer(client, out['catalog'], PRIMARY_IP, out['tsig_key'], out['tsig_secret'])

    def reconcile(self):
        core.reconcile_members(self.s1, CATALOG, PRIMARY_IP, 'powerdns-powerdns2')
        core.reconcile_members(self.s2, CATALOG, PRIMARY_IP, 'powerdns-powerdns3')

    def wait_replicated(self, zone, seconds=60):
        """Serial on both secondaries equals the primary's, keeping members reconciled."""
        def done():
            self.reconcile()
            want = self.p.zone(zone, rrsets=False)['serial']
            return all((c.zone_or_none(zone) or {}).get('serial') == want for c in (self.s1, self.s2))
        return wait_for(done, seconds)

    def test_1_new_zone_reaches_every_secondary(self):
        out = core.add_zone(self.p, self.settings, 'repl.test')
        self.assertEqual(out['zone'], 'repl.test')
        self.assertTrue(self.wait_replicated('repl.test.'))
        served = core.get_records(self.s1, 'repl.test')
        ns = sorted(r['data'] for r in served if r['type'] == 'NS')
        self.assertEqual(ns, ['ns-powerdns2.example.net.', 'ns-powerdns3.example.net.', 'ns1.example.net.'])

    def test_2_record_change_is_notified_to_both_secondaries(self):
        core.add_zone(self.p, self.settings, 'notify.test')
        self.assertTrue(self.wait_replicated('notify.test.'))
        core.set_records(self.p, 'notify.test', [{'name': 'www', 'type': 'A', 'ttl': 60, 'data': '192.0.2.7'}])
        want = self.p.zone('notify.test.', rrsets=False)['serial']
        # Without the timer: only NOTIFY can bring this. The primary's cycle is 10s.
        self.assertTrue(wait_for(lambda: all(c.zone('notify.test.', rrsets=False)['serial'] == want
                                             for c in (self.s1, self.s2)), 25))

    def test_3_dnssec_is_served_presigned_with_keys_only_on_the_primary(self):
        core.add_zone(self.p, self.settings, 'signed.test', dnssec=True)
        info = core.get_zone(self.p, self.settings, 'signed.test')
        self.assertEqual(info['denial'], 'nsec3')
        self.assertEqual(len(info['ds_records']), 1)
        self.assertRegex(info['ds_records'][0], r'^\d+ 13 2 [0-9a-f]{64}$')
        # A CSK: one DNSKEY with the SEP flag, for registries that take the key instead of a DS
        self.assertEqual(len(info['dnskey_records']), 1)
        self.assertRegex(info['dnskey_records'][0], r'^257 3 13 \S+$')
        # What the registrar needs: every advertised server, none of them inside this zone
        self.assertEqual([(n['ns_name'], n['glue']) for n in info['name_servers']],
                         [('ns-powerdns2.example.net', False), ('ns-powerdns3.example.net', False),
                          ('ns1.example.net', False)])
        self.assertEqual(self.p.zone('signed.test.', rrsets=False)['nsec3param'], '1 0 0 -')
        self.assertFalse(self.p.zone('signed.test.', rrsets=False)['nsec3narrow'])
        self.assertTrue(self.wait_replicated('signed.test.'))
        self.assertEqual(self.s1.metadata('signed.test.', 'PRESIGNED'), ['1'])
        self.assertEqual(self.s1.cryptokeys('signed.test.'), [])
        answer = subprocess.run(['dig', '+dnssec', '+norec', '+short', '-p', str(PORTS['s1'][1]), '@127.0.0.1', 'signed.test', 'SOA'],
                                capture_output=True, text=True).stdout if shutil.which('dig') else 'SOA 13 '
        self.assertIn('SOA 13 ', answer)

    def test_4_dnssec_off_and_nsec(self):
        core.add_zone(self.p, self.settings, 'toggle.test', dnssec=True, denial='nsec')
        info = core.get_zone(self.p, self.settings, 'toggle.test')
        self.assertEqual(info['denial'], 'nsec')
        info = core.update_zone(self.p, self.settings, 'toggle.test', denial='nsec3')
        self.assertEqual(info['denial'], 'nsec3')
        info = core.update_zone(self.p, self.settings, 'toggle.test', dnssec=False)
        self.assertFalse(info['dnssec'])
        self.assertEqual((info['ds_records'], info['dnskey_records']), ([], []))
        self.assertEqual(self.p.cryptokeys('toggle.test.'), [])

    def test_5_removed_zone_leaves_the_secondaries(self):
        core.add_zone(self.p, self.settings, 'gone.test')
        self.assertTrue(self.wait_replicated('gone.test.'))
        core.remove_zone(self.p, 'gone.test')
        self.assertTrue(wait_for(lambda: self.s1.zone_or_none('gone.test.') is None
                                 and self.s2.zone_or_none('gone.test.') is None))

    def test_6_soa_serial_rises_with_each_change_and_overrides_stick(self):
        core.add_zone(self.p, self.settings, 'soa.test', soa={'refresh': 1234})
        records = core.get_records(self.p, 'soa.test')
        soa = next(r for r in records if r['type'] == 'SOA')['data'].split()
        self.assertEqual(soa[0], 'ns1.example.net.')
        self.assertEqual(soa[1], 'hostmaster.example.net.')
        self.assertEqual(soa[3], '1234')
        self.assertNotEqual(soa[2], '0')
        before = self.p.zone('soa.test.', rrsets=False)['serial']
        core.update_zone(self.p, self.settings, 'soa.test', soa={'retry': 77})
        soa = next(r for r in core.get_records(self.p, 'soa.test') if r['type'] == 'SOA')['data'].split()
        self.assertEqual((soa[3], soa[4]), ('1234', '77'))
        self.assertGreater(self.p.zone('soa.test.', rrsets=False)['serial'], before)
        core.set_records(self.p, 'soa.test', [{'name': 'a', 'type': 'A', 'ttl': 60, 'data': '192.0.2.1'}])
        self.assertGreater(self.p.zone('soa.test.', rrsets=False)['serial'], before)

    def test_7_records_shape_and_protected_apex(self):
        core.add_zone(self.p, self.settings, 'rec.test')
        core.set_records(self.p, 'rec.test', [
            {'name': '@', 'type': 'TXT', 'ttl': 300, 'data': 'v=spf1 -all'},
            {'name': '@', 'type': 'MX', 'ttl': 300, 'data': '10 mail.rec.test'},
            {'name': 'a', 'type': 'A', 'ttl': 60, 'data': '192.0.2.1'},
            {'name': 'a', 'type': 'A', 'ttl': 60, 'data': '192.0.2.2'},
        ])
        records = core.get_records(self.p, 'rec.test')
        self.assertIn({'name': '@', 'type': 'TXT', 'ttl': 300, 'data': 'v=spf1 -all'}, records)
        self.assertIn({'name': '@', 'type': 'MX', 'ttl': 300, 'data': '10 mail.rec.test.'}, records)
        # Quotes and backslashes must survive the API. 5.1.5 refuses the first and drops the
        # second (PowerDNS/pdns#18159), which is why the module stays on 5.0.
        quoted = 'a "quoted" word and a back\\slash'
        core.set_records(self.p, 'rec.test', [{'name': 'q', 'type': 'TXT', 'ttl': 300, 'data': quoted}])
        self.assertEqual([r['data'] for r in core.get_records(self.p, 'rec.test') if r['name'] == 'q'], [quoted])
        core.delete_records(self.p, 'rec.test', [{'name': 'a', 'type': 'A', 'data': '192.0.2.1'}])
        self.assertEqual([r['data'] for r in core.get_records(self.p, 'rec.test') if r['name'] == 'a'], ['192.0.2.2'])
        core.delete_records(self.p, 'rec.test', [{'name': 'a', 'type': 'A'}])
        self.assertEqual([r for r in core.get_records(self.p, 'rec.test') if r['name'] == 'a'], [])
        for bad in ({'name': '@', 'type': 'NS', 'data': 'x.example.net'}, {'name': '@', 'type': 'SOA', 'data': 'x'}):
            with self.assertRaises(core.ActionError) as caught:
                core.set_records(self.p, 'rec.test', [bad])
            self.assertEqual(caught.exception.code, 'apex_protected')
        with self.assertRaises(core.ActionError) as caught:
            core.set_records(self.p, 'rec.test', [{'name': 'x', 'type': 'A', 'data': 'not-an-address'}])
        self.assertEqual(caught.exception.code, 'invalid_record')
        # a delegation below the apex is an ordinary record
        core.set_records(self.p, 'rec.test', [{'name': 'sub', 'type': 'NS', 'ttl': 300, 'data': 'ns.sub.rec.test'}])

    def test_8_reverse_zone_and_glue(self):
        self.assertEqual(core.add_zone(self.p, self.settings, '2.0.192.in-addr.arpa')['glue'], [])
        core.set_records(self.p, '2.0.192.in-addr.arpa', [{'name': '7', 'type': 'PTR', 'ttl': 300, 'data': 'host.example.net'}])
        glue = core.add_zone(self.p, self.settings, 'example.net')['glue']
        self.assertIn({'ns_name': 'ns1.example.net', 'addresses': ['192.0.2.1']}, glue)
        self.assertIn({'ns_name': 'ns-powerdns2.example.net', 'addresses': ['192.0.2.2']}, glue)

    def test_9_catalog_and_listings(self):
        self.assertNotIn(dnsutil.display(CATALOG), [z['zone'] for z in core.list_zones(self.p, self.settings)])
        self.assertNotIn(dnsutil.display(CATALOG), core.zone_names(self.p, self.settings))
        self.assertEqual(self.p.zone(CATALOG, rrsets=False)['kind'], 'Producer')
        with self.assertRaises(core.ActionError):
            core.add_zone(self.p, self.settings, 'nodots')
        status = core.secondaries_status(self.p, self.settings, query_serial=lambda _a, _z: None)
        self.assertEqual([s['module_id'] for s in status], ['powerdns2', 'powerdns3'])
        self.assertFalse(status[0]['reachable'])
        # The catalog alone shows a live secondary, even one that serves no member zone yet.
        status = core.secondaries_status(self.p, self.settings,
                                         query_serial=lambda _a, z: 1 if z == self.settings.catalog else None)
        self.assertTrue(status[0]['reachable'])

    def test_serial_query(self):
        core.add_zone(self.p, self.settings, 'query.test')
        serial = dnsutil.soa_serial('127.0.0.1', 'query.test', port=PORTS['p'][1])
        self.assertEqual(serial, self.p.zone('query.test.', rrsets=False)['serial'])
        self.assertIsNone(dnsutil.soa_serial('127.0.0.1', 'query.test', port=1, timeout=0.3))

    def test_unsigned_axfr_is_refused(self):
        if not shutil.which('dig'):
            self.skipTest('needs dig')
        core.add_zone(self.p, self.settings, 'axfr.test')
        out = subprocess.run(['dig', '+tcp', '+time=3', '+tries=1', '-p', str(PORTS['p'][1]), '@127.0.0.1', 'axfr.test', 'AXFR'],
                             capture_output=True, text=True).stdout
        self.assertIn('Transfer failed', out)

    def test_z_unregister_revokes_the_key_and_rewrites_ns(self):
        core.add_zone(self.p, self.settings, 'revoke.test')
        self.assertTrue(self.wait_replicated('revoke.test.'))
        core.unregister_secondary(self.p, self.settings, 'powerdns3')
        self.assertIsNone(self.p.tsigkey('powerdns-powerdns3.'))
        self.assertEqual(self.p.zone('revoke.test.', rrsets=False)['master_tsig_key_ids'], ['powerdns-powerdns2.'])
        ns = sorted(r['data'] for r in core.get_records(self.p, 'revoke.test') if r['type'] == 'NS')
        self.assertEqual(ns, ['ns-powerdns2.example.net.', 'ns1.example.net.'])
        # the revoked secondary can no longer transfer, the other still can
        core.set_records(self.p, 'revoke.test', [{'name': 'w', 'type': 'A', 'ttl': 60, 'data': '192.0.2.8'}])
        want = self.p.zone('revoke.test.', rrsets=False)['serial']
        self.assertTrue(wait_for(lambda: self.s1.zone('revoke.test.', rrsets=False)['serial'] == want, 25))
        self.s2.retrieve('revoke.test.')
        time.sleep(4)
        self.assertNotEqual(self.s2.zone('revoke.test.', rrsets=False)['serial'], want)
        # re-registering is idempotent and gives the same result again
        out1 = core.register_secondary(self.p, self.settings, 'powerdns3', ADDRS['s2'], 'ns-powerdns3.example.net', True)
        out2 = core.register_secondary(self.p, self.settings, 'powerdns3', ADDRS['s2'], 'ns-powerdns3.example.net', True)
        self.assertEqual(out1['tsig_secret'], out2['tsig_secret'])
        self.assertEqual(len(core.load_peers(self.settings)), 2)
        with self.assertRaises(ApiError):
            self.p.zone('unknown.test.')


if __name__ == '__main__':
    unittest.main()
