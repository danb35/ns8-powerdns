#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""The instance's configuration, its files and the rendered pdns.conf.

Settings are plain variables in state/environment (never secrets, DESIGN 8.1).
agent.set_env() does not update os.environ, and an action step may need a value
an earlier step just wrote, so they are always read from the file.
"""

import json
import os

ENV_VARS = (
    'POWERDNS_ROLE', 'NS_NAME', 'ADVERTISE', 'LISTEN_ADDRESSES', 'HOSTMASTER',
    'SOA_REFRESH', 'SOA_RETRY', 'SOA_EXPIRE', 'SOA_MINIMUM',
    'PRIMARY_MODULE_UUID', 'PRIMARY_ADDRESS', 'CATALOG_NAME',
)

SOA_DEFAULTS = {'refresh': 10800, 'retry': 3600, 'expire': 604800, 'minimum': 3600}

# PowerDNS applies per-zone ALSO-NOTIFY when the primary's update check runs, so
# this interval is the upper bound on how long a change takes to leave the
# primary (the default of 60 seconds would miss DESIGN 11's "within seconds").
PRIMARY_XFR_CYCLE_SECONDS = 10


def state_dir():
    return os.environ.get('AGENT_STATE_DIR') or os.getcwd()


def path(*parts):
    return os.path.join(state_dir(), *parts)


def read_envfile(file_path):
    values = {}
    try:
        with open(file_path) as fp:
            for line in fp:
                line = line.rstrip('\n')
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    values[key] = value
    except FileNotFoundError:
        pass
    return values


def env():
    return read_envfile(path('environment'))


def secrets():
    return read_envfile(path('passwords.env'))


def write_secrets(values):
    """Merge values into state/passwords.env, created 0600 before any secret is written."""
    merged = secrets()
    merged.update(values)
    write_private(path('passwords.env'), ''.join('%s=%s\n' % kv for kv in sorted(merged.items())))


def write_private(file_path, content):
    tmp = '%s.%d.tmp' % (file_path, os.getpid())
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as fp:
        fp.write(content)
    os.replace(tmp, file_path)


def read_json(file_path, default):
    try:
        with open(file_path) as fp:
            return json.load(fp)
    except FileNotFoundError:
        return default


def write_json(file_path, value):
    write_private(file_path, json.dumps(value, indent=1, sort_keys=True) + '\n')


def is_standby():
    return os.path.exists(path('standby'))


def set_standby(active):
    if active:
        with open(path('standby'), 'w'):
            pass
    else:
        try:
            os.remove(path('standby'))
        except FileNotFoundError:
            pass


def listen_addresses(values):
    return [a for a in values.get('LISTEN_ADDRESSES', '').split(',') if a]


def soa_timers(values):
    return {k: int(values.get('SOA_' + k.upper()) or SOA_DEFAULTS[k]) for k in SOA_DEFAULTS}


def render_pdns_conf(role, addresses, vpn_address, cluster_network, tcp_port, api_key, primary_address=''):
    """The whole pdns.conf. Every value here comes from a checked source (DESIGN 4, 6, 7)."""
    lines = [
        'launch=gsqlite3',
        'gsqlite3-database=/var/lib/powerdns/pdns.sqlite3',
        'gsqlite3-dnssec=yes',
        'local-port=53',
        'local-address=' + ','.join(addresses),
        # Authoritative only: nothing here may turn it into a resolver.
        'version-string=anonymous',
        # The API key is the only thing in this file that is secret.
        'api=yes',
        'webserver=yes',
        'api-key=' + api_key,
        'webserver-port=%s' % tcp_port,
        # An empty list means an AXFR needs a TSIG key that the zone allows. With
        # the default, or with the VPN network here, an unsigned request from a
        # listed address would be accepted without any key (DESIGN 6.3).
        'allow-axfr-ips=',
    ]
    if role == 'primary':
        lines += [
            'primary=yes',
            # webserver-address takes a single address, so this is the VPN address
            # alone and local actions call the API on it too (DESIGN 4.4).
            'webserver-address=' + vpn_address,
            'webserver-allow-from=127.0.0.1,::1,' + cluster_network,
            # A NOTIFY is signed with the zone's first TSIG-ALLOW-AXFR key, and a
            # secondary refuses any other key: with per-secondary keys all
            # secondaries but one would ignore it. An unsigned NOTIFY from the
            # primary's address grants nothing, it only prompts a signed SOA check.
            'send-signed-notify=no',
            # Notify only the registered peers (ALSO-NOTIFY), not whatever the
            # zone's NS names resolve to on the public network.
            'only-notify=',
            'xfr-cycle-interval=%d' % PRIMARY_XFR_CYCLE_SECONDS,
            # One combined signing key, algorithm 13 (DESIGN 7.1).
            'default-ksk-algorithm=ecdsa256',
            'default-zsk-algorithm=',
        ]
    else:
        lines += [
            'secondary=yes',
            'webserver-address=127.0.0.1',
            'webserver-allow-from=127.0.0.1,::1',
            'allow-notify-from=' + (primary_address + '/32' if primary_address else ''),
        ]
    return '\n'.join(lines) + '\n'
