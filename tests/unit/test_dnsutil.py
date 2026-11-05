#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'imageroot', 'pypkg'))

from pdnsmodule import config, dnsutil


class Names(unittest.TestCase):
    def test_canonical_and_relative(self):
        self.assertEqual(dnsutil.canonical('Example.COM'), 'example.com.')
        self.assertEqual(dnsutil.relative_name('www.example.com.', 'example.com'), 'www')
        self.assertEqual(dnsutil.relative_name('example.com.', 'example.com'), '@')
        self.assertEqual(dnsutil.absolute_name('@', 'example.com'), 'example.com.')
        self.assertEqual(dnsutil.absolute_name('www', 'example.com.'), 'www.example.com.')

    def test_is_dns_name(self):
        for good in ('example.com', '10.in-addr.arpa', 'example.com.', '_sub.example.org'):
            self.assertTrue(dnsutil.is_dns_name(good), good)
        for bad in ('', 'nodots', '-bad.example.com', 'a..b', 'sp ace.example.com', 'x' * 64 + '.com'):
            self.assertFalse(dnsutil.is_dns_name(bad), bad)

    def test_subdomain_needs_a_label_boundary(self):
        self.assertTrue(dnsutil.is_subdomain('ns1.example.com', 'example.com'))
        self.assertFalse(dnsutil.is_subdomain('ns1.notexample.com', 'example.com'))

    def test_soa_rname(self):
        self.assertEqual(dnsutil.soa_rname('hostmaster@example.com'), 'hostmaster.example.com.')
        self.assertEqual(dnsutil.soa_rname('first.last@example.com'), 'first\\.last.example.com.')
        self.assertEqual(dnsutil.soa_rname('hostmaster.example.com'), 'hostmaster.example.com.')


class Presentation(unittest.TestCase):
    def test_txt_round_trip(self):
        for value in ('v=spf1 -all', 'quote " and \\ slash', 'x' * 700, 'é' * 300, ''):
            self.assertEqual(dnsutil.txt_unquote(dnsutil.txt_quote(value)), value)

    def test_long_txt_is_split_without_breaking_characters(self):
        quoted = dnsutil.txt_quote('é' * 300)
        for chunk in quoted.split(' '):
            self.assertLessEqual(len(chunk.strip('"').encode()), 255)

    def test_targets_get_a_final_dot(self):
        self.assertEqual(dnsutil.to_presentation('MX', '10 mail.example.com'), '10 mail.example.com.')
        self.assertEqual(dnsutil.to_presentation('SRV', '0 0 443 a.example.com.'), '0 0 443 a.example.com.')
        self.assertEqual(dnsutil.to_presentation('PTR', 'host.example.com'), 'host.example.com.')
        self.assertEqual(dnsutil.to_presentation('A', '192.0.2.1'), '192.0.2.1')


class PdnsConf(unittest.TestCase):
    def conf(self, role, **kw):
        lines = config.render_pdns_conf(role, ['192.0.2.1', '10.5.4.1'], '10.5.4.1', '10.5.4.0/24', 20001, 'KEY', **kw).splitlines()
        return dict(line.split('=', 1) for line in lines)

    def test_primary(self):
        conf = self.conf('primary')
        self.assertEqual(conf['local-address'], '192.0.2.1,10.5.4.1')
        self.assertEqual(conf['webserver-address'], '10.5.4.1')
        self.assertEqual(conf['allow-axfr-ips'], '')
        self.assertEqual(conf['send-signed-notify'], 'no')
        self.assertEqual(conf['only-notify'], '')
        self.assertEqual(conf['default-zsk-algorithm'], '')
        self.assertEqual(conf['security-poll-suffix'], '')
        self.assertNotIn('0.0.0.0', ''.join(conf.values()))

    def test_secondary_keeps_its_api_on_loopback(self):
        conf = self.conf('secondary', primary_address='10.5.4.1')
        self.assertEqual(conf['webserver-address'], '127.0.0.1')
        self.assertEqual(conf['security-poll-suffix'], '')
        self.assertEqual(conf['allow-notify-from'], '10.5.4.1/32')
        self.assertEqual(conf['allow-axfr-ips'], '')
        self.assertNotIn('primary', conf)


if __name__ == '__main__':
    unittest.main()
