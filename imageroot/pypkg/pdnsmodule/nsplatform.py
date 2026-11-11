#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""Everything that touches the NS8 node or Redis."""

import errno
import fcntl
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time

import agent
import agent.tasks

from . import config, core, dnsutil
from .pdnsapi import Pdns

API_SERVICE = 'powerdns-api'
UNIT = 'powerdns.service'
CATALOG_WAIT_SECONDS = 15

# Interfaces that never carry a public service.
_SKIP_INTERFACES = ('lo', 'wg', 'podman', 'cni', 'veth', 'docker', 'br-')


def log(message, level=None):
    print((level if level is not None else agent.SD_INFO) + 'powerdns: ' + message, file=sys.stderr)


def redis():
    """The leader when it is reachable, so a primary installed a moment ago counts.

    A replica may lag behind on a node just added to the cluster (DESIGN 3).
    """
    rdb = agent.redis_connect()
    try:
        rdb.ping()
    except Exception:
        log('cluster leader unreachable, using the local replica', agent.SD_WARNING)
        rdb = agent.redis_connect(use_replica=True)
    return rdb


def vpn_address(rdb):
    return rdb.hget('node/%s/vpn' % os.environ['NODE_ID'], 'ip_address')


def cluster_network(rdb):
    return rdb.get('cluster/network')


def primaries(rdb):
    return agent.list_service_providers(rdb, API_SERVICE, 'tcp')


def other_primaries(rdb):
    return [p for p in primaries(rdb) if p.get('module_id') != os.environ['MODULE_ID']]


def service_key():
    return 'module/%s/srv/tcp/%s' % (os.environ['MODULE_ID'], API_SERVICE)


def publish(event):
    payload = {'module_id': os.environ['MODULE_ID'], 'module_uuid': os.environ.get('MODULE_UUID', '')}
    try:
        agent.redis_connect(privileged=True).publish('%s/event/%s' % (os.environ['AGENT_ID'], event), json.dumps(payload))
    except Exception as e:
        log('cannot publish %s: %s' % (event, e), agent.SD_WARNING)


def register_service(rdb):
    """Write the service key; tell dnshelper when what it holds went stale."""
    wanted = {'host': vpn_address(rdb), 'port': os.environ['TCP_PORT'], 'role': 'primary'}
    writer = agent.redis_connect(privileged=True)
    if writer.hgetall(service_key()) != wanted:
        writer.hset(service_key(), mapping=wanted)
        publish('powerdns-provider-changed')


def unregister_service():
    agent.redis_connect(privileged=True).delete(service_key())


def api_client(values=None):
    """On a primary the API listens on the VPN address, on a secondary on loopback."""
    values = values if values is not None else config.env()
    if values.get('POWERDNS_ROLE') == 'primary':
        host = vpn_address(agent.redis_connect(use_replica=True))
    else:
        host = '127.0.0.1'
    return Pdns('http://%s:%s' % (host, os.environ['TCP_PORT']), config.secrets()['PDNS_API_KEY'])


def settings(values=None):
    values = values if values is not None else config.env()
    return core.Settings(
        module_id=os.environ['MODULE_ID'],
        ns_name=values.get('NS_NAME', ''),
        advertise=values.get('ADVERTISE', 'true') == 'true',
        hostmaster=values.get('HOSTMASTER', ''),
        soa=config.soa_timers(values),
        catalog=values.get('CATALOG_NAME', ''),
        addresses=config.listen_addresses(values),
        peers_file=config.path('peers.json'),
    )


class peers_lock:
    """Register, unregister and the reconcile timer must not interleave."""

    def __enter__(self):
        self.fp = open(config.path('.peers.lock'), 'w')
        fcntl.flock(self.fp, fcntl.LOCK_EX)
        return self

    def __exit__(self, *_exc):
        self.fp.close()


# --- a copy on the same node as its original (DESIGN 10) --------------------

def sibling_instances(rdb):
    """Other powerdns instances on this node. They hold port 53 on the VPN address."""
    nodes = rdb.hgetall('cluster/module_node')
    return sorted(m for m, node in nodes.items()
                  if re.fullmatch(r'powerdns[0-9]+', m) and m != os.environ['MODULE_ID']
                  and str(node) == str(os.environ['NODE_ID']))


def start_blocked(rdb=None):
    """A copy cannot run while its original is on this node: both need the same port.

    The core removes the original only after the copy's restore or clone has
    succeeded, so the copy must finish without starting. Reconcile starts it.
    """
    return config.is_copy_pending() and bool(sibling_instances(rdb or redis()))


# --- node addresses and port 53 (DESIGN 4.1) --------------------------------

def node_addresses():
    """The node's global unicast addresses, with the interfaces that carry services."""
    # A module user's PATH may lack /usr/sbin
    ip = shutil.which('ip') or '/usr/sbin/ip'
    out = subprocess.run([ip, '-j', 'addr', 'show'], capture_output=True, text=True, check=True).stdout
    addresses = []
    for iface in json.loads(out):
        if iface['ifname'].startswith(_SKIP_INTERFACES):
            continue
        for addr in iface.get('addr_info', []):
            if addr.get('scope') == 'global':
                addresses.append(addr['local'])
    return addresses


def _port_free(address, kind):
    family = socket.AF_INET6 if ':' in address else socket.AF_INET
    with socket.socket(family, kind) as sock:
        # Only for TCP, where it skips sockets in TIME_WAIT. On a UDP socket it lets the probe bind
        # next to another server's reuse-enabled socket (dnsmasq's), so a busy port read as free.
        if kind == socket.SOCK_STREAM:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((address, 53))
        except OSError as e:
            if e.errno in (errno.EADDRINUSE, errno.EACCES):
                return False
            raise
    return True


def service_active():
    return subprocess.run(['systemctl', '--user', 'is-active', '--quiet', UNIT], check=False).returncode == 0


def port53_report(address, ours):
    """Whether this instance could bind 53 here. `ours` are addresses it holds itself."""
    if address in ours:
        return {'address': address, 'udp_free': True, 'tcp_free': True, 'in_use_by_self': True}
    return {'address': address, 'udp_free': _port_free(address, socket.SOCK_DGRAM),
            'tcp_free': _port_free(address, socket.SOCK_STREAM), 'in_use_by_self': False}


def addresses_held(values, vpn):
    """The addresses our own running server occupies, so they do not read as busy."""
    if not service_active():
        return []
    return config.listen_addresses(values) + ([vpn] if vpn else [])


# --- dnshelper (DESIGN 8.3) -------------------------------------------------

def dnshelper_modules(rdb=None):
    """Every dnshelper instance in the cluster. Any of them may have adopted this primary's zones."""
    nodes = (rdb or redis()).hgetall('cluster/module_node')
    return sorted((m for m in nodes if re.fullmatch(r'dnshelper[0-9]+', m)), key=lambda m: int(m[9:]))


def dnshelper_module(rdb=None):
    """The cluster's default dnshelper, or else the first one installed."""
    try:
        agent_id = agent.resolve_agent_id('dnshelper@cluster')
    except Exception:
        agent_id = None
    if agent_id:
        return agent_id.removeprefix('module/')
    modules = dnshelper_modules(rdb)
    return modules[0] if modules else None


def _dnshelper_manages(module_id, zone):
    try:
        response = agent.tasks.run('module/' + module_id, action='has-zone', data={'name': dnsutil.display(zone)},
                                   extra={'isNotificationHidden': True})
    except Exception as e:
        log('has-zone on %s failed: %s' % (module_id, e), agent.SD_WARNING)
        return False
    if response.get('exit_code') != 0:
        return False
    output = response.get('output') or {}
    return bool(output.get('managed')) and dnsutil.canonical(output.get('zone') or '') == dnsutil.canonical(zone)


def zone_manager(zone, rdb=None):
    """The dnshelper instance that manages the zone, or None.

    Every instance is asked, not only the cluster default. No answer means not managed: a removed
    dnshelper must not lock zones.
    """
    return next((m for m in dnshelper_modules(rdb) if _dnshelper_manages(m, zone)), None)


def managed_by_dnshelper(zone):
    return zone_manager(zone) is not None


# --- replication, secondary side (DESIGN 6.2) -------------------------------

def register_with_primary(values, primary, restart_on_address_change=True):
    """Register on the primary, then store the key and make PowerDNS follow the catalog."""
    module_id = os.environ['MODULE_ID']
    response = agent.tasks.run('module/' + primary['module_id'], action='register-secondary', data={
        'module_id': module_id,
        'address': vpn_address(redis()),
        'ns_name': values.get('NS_NAME', ''),
        'advertise': values.get('ADVERTISE', 'true') == 'true',
        'addresses': config.listen_addresses(values),
    }, extra={'isNotificationHidden': True})
    if response.get('exit_code') != 0:
        raise core.ActionError('primary', 'registration_failed', primary['module_id'], str(response.get('error', ''))[:200])
    output = response['output']
    config.write_secrets({'TSIG_KEY_NAME': output['tsig_key'], 'TSIG_KEY_SECRET': output['tsig_secret'],
                          'TSIG_KEY_OWNER': module_id})
    changed = values.get('PRIMARY_ADDRESS') != primary['host']
    agent.mset_env({'CATALOG_NAME': output['catalog'], 'PRIMARY_MODULE_UUID': primary['module_uuid'],
                    'PRIMARY_ADDRESS': primary['host']})
    if changed and restart_on_address_change:
        # allow-notify-from is read at start
        subprocess.run(['systemctl', '--user', 'try-restart', UNIT], check=True)
    pdns = api_client(config.env())
    pdns.wait_ready()
    core.ensure_consumer(pdns, output['catalog'], primary['host'], output['tsig_key'], output['tsig_secret'])
    # The members exist once the catalog has arrived, usually within a second or
    # two. Do not leave them to the next timer run, with their first transfers refused.
    for _ in range(CATALOG_WAIT_SECONDS):
        if (pdns.zone_or_none(output['catalog']) or {}).get('serial'):
            break
        time.sleep(1)
    core.reconcile_members(pdns, output['catalog'], primary['host'], output['tsig_key'])


def unregister_from_primary():
    """Best effort: if it fails the primary's Replication page offers a Remove button."""
    module_id = os.environ['MODULE_ID']
    values = config.env()
    try:
        found = [p for p in primaries(redis()) if p.get('module_uuid') == values.get('PRIMARY_MODULE_UUID')] or primaries(redis())
        if not found:
            return
        agent.tasks.run('module/' + found[0]['module_id'], action='unregister-secondary',
                        data={'module_id': module_id}, extra={'isNotificationHidden': True})
    except Exception as e:
        log('cannot unregister from the primary: %s' % e, agent.SD_WARNING)


# --- reconcile: timer, after configure, after a clone or restore ------------

def leave_standby_if_possible(rdb):
    if config.is_standby() and not other_primaries(rdb):
        config.set_standby(False)
        register_service(rdb)
        log('no other primary exists: leaving standby')
        for event in ('powerdns-replication-changed', 'powerdns-provider-changed', 'powerdns-zones-changed'):
            publish(event)


def ensure_soa_edit(values):
    """Once per instance: zones created by 0.1.1 and earlier have no SOA-EDIT (core.SOA_EDIT).

    The marker is left out of the backup, so a restore or clone of an old
    backup checks its zones again.
    """
    marker = config.path('soa-edit-applied')
    if os.path.exists(marker):
        return
    pdns = api_client(values)
    fixed = core.ensure_soa_edit(pdns, settings(values))
    if fixed:
        log('set SOA-EDIT on: %s' % ', '.join(fixed))
    with open(marker, 'w'):
        pass


def reconcile(values=None):
    values = values if values is not None else config.env()
    role = values.get('POWERDNS_ROLE')
    if not role:
        return
    rdb = redis()
    if config.is_copy_pending():
        if sibling_instances(rdb):
            return
        config.set_copy_pending(False)
        if not service_active():
            log('no other instance on this node: starting')
            subprocess.run(['systemctl', '--user', 'enable', '--now', UNIT], check=True)
            api_client(values).wait_ready()
    if role == 'primary':
        leave_standby_if_possible(rdb)
        if not config.is_standby():
            ensure_soa_edit(values)
            register_service(rdb)
            if other_primaries(rdb):
                log('another primary is registered: %s' % ', '.join(p['module_id'] for p in other_primaries(rdb)), agent.SD_WARNING)
        return
    found = primaries(rdb)
    if len(found) != 1:
        return  # none, or more than one (DESIGN 8.4): keep serving what we have
    primary = found[0]
    secrets = config.secrets()
    stale = (secrets.get('TSIG_KEY_OWNER') != os.environ['MODULE_ID'] or not secrets.get('TSIG_KEY_SECRET')
             or values.get('PRIMARY_ADDRESS') != primary['host'])
    with peers_lock():
        if stale:
            log('registering with %s' % primary['module_id'])
            register_with_primary(values, primary)
        else:
            fixed = core.reconcile_members(api_client(values), values['CATALOG_NAME'], values['PRIMARY_ADDRESS'], secrets['TSIG_KEY_NAME'])
            if fixed:
                log('set the transfer key on: %s' % ', '.join(fixed))
