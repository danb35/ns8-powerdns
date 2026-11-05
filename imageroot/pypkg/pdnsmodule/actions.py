#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""Action entry points. Each imageroot/actions/<name>/ has a stub calling run()."""

import json
import os
import secrets as pysecrets
import subprocess
import sys

import agent

from . import config, core, dnsutil, nsplatform as ns
from .pdnsapi import ApiError

PUBLIC_RESOLVERS = ('1.1.1.1', '9.9.9.9')


def _require_primary(values, write=True):
    if values.get('POWERDNS_ROLE') != 'primary':
        raise core.ActionError('role', 'not_a_primary', values.get('POWERDNS_ROLE', ''))
    if write and config.is_standby():
        # A standby copy holds the same zones as the real primary: diverging from
        # it would lose changes when one of them goes away.
        raise core.ActionError('role', 'primary_standby', os.environ['MODULE_ID'])


def _require_configured(values):
    if not values.get('POWERDNS_ROLE'):
        raise core.ActionError('role', 'not_configured', '')


# --- configure-module -------------------------------------------------------

def configure_validate(request):
    values = config.env()
    role = request['role']
    module_id = os.environ['MODULE_ID']
    rdb = ns.redis()
    previous = values.get('POWERDNS_ROLE')
    if previous and previous != role:
        raise core.ActionError('role', 'role_change_not_supported', role)
    if role == 'primary' and not config.is_standby():
        others = ns.other_primaries(rdb)
        if others:
            raise core.ActionError('role', 'primary_exists', role, others[0]['module_id'])
    primary = None
    if role == 'secondary':
        primary = next((p for p in ns.primaries(rdb) if p.get('module_uuid') == request.get('primary')), None)
        if primary is None:
            raise core.ActionError('primary', 'primary_not_found', request.get('primary', ''))
        if primary['module_id'] == module_id:
            raise core.ActionError('primary', 'primary_is_self', request.get('primary', ''))
    if not dnsutil.is_dns_name(request['ns_name']):
        raise core.ActionError('ns_name', 'invalid_ns_name', request['ns_name'])
    if role == 'primary' and not request.get('hostmaster'):
        raise core.ActionError('hostmaster', 'hostmaster_required', '')
    vpn = ns.vpn_address(rdb)
    available = ns.node_addresses()
    held = ns.addresses_held(values, vpn)
    for address in request.get('listen_addresses', []):
        if address not in available:
            raise core.ActionError('listen_addresses', 'address_not_on_node', address)
    if ns.start_blocked(rdb):
        return primary  # the original holds these addresses until it is removed
    for address in request.get('listen_addresses', []) + [vpn]:
        report = ns.port53_report(address, held)
        if not (report['udp_free'] and report['tcp_free']):
            raise core.ActionError('listen_addresses', 'address_busy', address)
    return primary


def configure_save(request):
    primary = configure_validate(request)
    values = config.env()
    update = {
        'POWERDNS_ROLE': request['role'],
        'NS_NAME': dnsutil.canonical(request['ns_name']).rstrip('.'),
        'ADVERTISE': 'true' if request.get('advertise', True) else 'false',
        'LISTEN_ADDRESSES': ','.join(request.get('listen_addresses', [])),
        'HOSTMASTER': request.get('hostmaster', ''),
    }
    for key, default in config.SOA_DEFAULTS.items():
        update['SOA_' + key.upper()] = str(request.get('soa_' + key) or values.get('SOA_' + key.upper()) or default)
    if request['role'] == 'primary':
        update['CATALOG_NAME'] = values.get('CATALOG_NAME') or core.catalog_name(os.environ['MODULE_UUID'])
    else:
        update['PRIMARY_MODULE_UUID'] = primary['module_uuid']
        update['PRIMARY_ADDRESS'] = primary['host']
    agent.mset_env(update)
    agent.assert_exp(agent.add_public_service(os.environ['MODULE_ID'], ['53/tcp', '53/udp'], replace_ports=True))


def configure_finalize(_request):
    values = config.env()
    if ns.start_blocked():
        ns.log('waiting for the other instance on this node to be removed')
        return
    pdns = ns.api_client(values)
    pdns.wait_ready()
    settings = ns.settings(values)
    if values['POWERDNS_ROLE'] == 'primary':
        with ns.peers_lock():
            core.ensure_catalog(pdns, settings)
            core.rewrite_apex_ns(pdns, settings)
        ns.reconcile(values)
    else:
        primary = next((p for p in ns.primaries(ns.redis()) if p.get('module_uuid') == values['PRIMARY_MODULE_UUID']), None)
        agent.assert_exp(primary is not None, 'the primary disappeared during configure-module')
        with ns.peers_lock():
            ns.register_with_primary(values, primary, restart_on_address_change=False)


def get_configuration(_request):
    values = config.env()
    rdb = ns.redis()
    vpn = ns.vpn_address(rdb)
    held = ns.addresses_held(values, vpn)
    primaries = ns.primaries(rdb)
    configured_addresses = config.listen_addresses(values)
    candidates = ns.node_addresses()
    timers = config.soa_timers(values)
    dnshelper = ns.dnshelper_module()
    return {
        'configured': bool(values.get('POWERDNS_ROLE')),
        'role': values.get('POWERDNS_ROLE', ''),
        'ns_name': values.get('NS_NAME', ''),
        'advertise': values.get('ADVERTISE', 'true') == 'true',
        'listen_addresses': configured_addresses,
        # Listen addresses that are not on this node (the module was cloned or moved)
        'missing_addresses': [a for a in configured_addresses if a not in candidates],
        'hostmaster': values.get('HOSTMASTER', ''),
        'soa_refresh': timers['refresh'], 'soa_retry': timers['retry'],
        'soa_expire': timers['expire'], 'soa_minimum': timers['minimum'],
        'primary': values.get('PRIMARY_MODULE_UUID', ''),
        'vpn_address': vpn,
        'standby': config.is_standby(),
        'node_addresses': [ns.port53_report(a, held) for a in candidates],
        'vpn_port': ns.port53_report(vpn, held),
        'primaries': [{'module_id': p['module_id'], 'module_uuid': p['module_uuid'], 'node': p.get('node'),
                       'ui_name': p.get('ui_name') or '', 'host': p['host']}
                      for p in primaries if p['module_id'] != os.environ['MODULE_ID']],
        'dnshelper': {'installed': bool(dnshelper), 'module_id': dnshelper or ''},
    }


# --- zones ------------------------------------------------------------------

def list_zones(_request):
    values = config.env()
    _require_configured(values)
    return {'zones': core.list_zones(ns.api_client(values), ns.settings(values))}


def add_zone(request):
    values = config.env()
    _require_primary(values)
    result = core.add_zone(ns.api_client(values), ns.settings(values), request['zone'],
                           dnssec=request.get('dnssec', False), denial=request.get('denial', 'nsec3'),
                           soa=_soa_overrides(request))
    ns.publish('powerdns-zones-changed')
    return result


def _soa_overrides(request):
    return {k: request['soa_' + k] for k in config.SOA_DEFAULTS if request.get('soa_' + k)}


def update_zone(request):
    values = config.env()
    _require_primary(values)
    return core.update_zone(ns.api_client(values), ns.settings(values), request['zone'],
                            dnssec=request.get('dnssec'), denial=request.get('denial'), soa=_soa_overrides(request))


def remove_zone(request):
    values = config.env()
    _require_primary(values)
    core.remove_zone(ns.api_client(values), request['zone'])
    ns.publish('powerdns-zones-changed')
    return {}


def get_zone(request):
    values = config.env()
    _require_configured(values)
    return core.get_zone(ns.api_client(values), ns.settings(values), request['zone'])


def check_zone_ds(request):
    """Informational, on demand: does a public resolver see a DS for the zone."""
    for resolver in PUBLIC_RESOLVERS:
        published = dnsutil.ds_published(resolver, request['zone'])
        if published is not None:
            return {'zone': request['zone'], 'published': published, 'resolver': resolver}
    return {'zone': request['zone'], 'published': None, 'resolver': ''}


# --- records ----------------------------------------------------------------

def get_records(request):
    values = config.env()
    _require_configured(values)
    zone = request['zone']
    is_primary = values['POWERDNS_ROLE'] == 'primary'
    manager = ns.zone_manager(zone) if is_primary else None
    managed = manager is not None
    dnshelper = manager or ns.dnshelper_module()
    return {
        'zone': zone,
        'records': core.get_records(ns.api_client(values), zone),
        'managed_by_dnshelper': managed,
        'dnshelper_module_id': dnshelper or '',
        'editable': is_primary and not managed and not config.is_standby(),
    }


def _refuse_if_managed(zone):
    if ns.managed_by_dnshelper(zone):
        raise core.ActionError('zone', 'managed_by_dnshelper', zone)


def set_records(request):
    values = config.env()
    _require_primary(values)
    _refuse_if_managed(request['zone'])
    return {'records': core.set_records(ns.api_client(values), request['zone'], request['records'])}


def delete_records(request):
    values = config.env()
    _require_primary(values)
    _refuse_if_managed(request['zone'])
    return {'records': core.delete_records(ns.api_client(values), request['zone'], request['records'])}


# --- replication ------------------------------------------------------------

def register_secondary(request):
    values = config.env()
    _require_primary(values)
    rdb = ns.redis()
    with ns.peers_lock():
        result = core.register_secondary(ns.api_client(values), ns.settings(values), request['module_id'], request['address'],
                                         request.get('ns_name', ''), request.get('advertise', True), request.get('addresses', []))
    result['primary_address'] = ns.vpn_address(rdb)
    return result


def unregister_secondary(request):
    values = config.env()
    _require_primary(values, write=False)
    with ns.peers_lock():
        core.unregister_secondary(ns.api_client(values), ns.settings(values), request['module_id'])
    return {}


def list_secondaries(_request):
    values = config.env()
    _require_primary(values, write=False)
    return {'secondaries': core.secondaries_status(ns.api_client(values), ns.settings(values))}


remove_secondary = unregister_secondary


# --- status -----------------------------------------------------------------

def get_dns_status(_request):
    """DNS state for the Status page; the service list comes from the core's get-status."""
    values = config.env()
    role = values.get('POWERDNS_ROLE', '')
    result = {'role': role, 'configured': bool(role), 'standby': config.is_standby(), 'service_active': ns.service_active(),
              'zones': [], 'secondaries': [], 'other_primaries': [], 'primary_reachable': None, 'api_ready': False,
              'waiting_for': []}
    if not role:
        return result
    rdb = ns.redis()
    if config.is_copy_pending():
        result['waiting_for'] = ns.sibling_instances(rdb)
    if role == 'primary':
        result['other_primaries'] = [p['module_id'] for p in ns.other_primaries(rdb)]
        # The status poll also ends a standby, as the reconcile timer does (DESIGN 10).
        ns.reconcile(values)
        result['standby'] = config.is_standby()
    if result['waiting_for']:
        return result
    try:
        pdns = ns.api_client(values)
        settings = ns.settings(values)
        if role == 'primary':
            result['zones'] = core.list_zones(pdns, settings)
            result['secondaries'] = core.secondaries_status(pdns, settings)
        else:
            address = values.get('PRIMARY_ADDRESS', '')
            result['zones'] = core.secondary_zones_status(pdns, address)
            result['primary_reachable'] = any(z['primary_serial'] is not None for z in result['zones']) if result['zones'] else None
        result['api_ready'] = True
    except (OSError, ApiError) as e:
        ns.log('PowerDNS is not answering: %s' % e, agent.SD_WARNING)
    return result


# --- dnshelper --------------------------------------------------------------

def get_provider_config(_request):
    values = config.env()
    _require_primary(values)
    rdb = ns.redis()
    pdns = ns.api_client(values)
    return {
        'provider': 'powerdns',
        'fields': {'api_url': 'http://%s:%s' % (ns.vpn_address(rdb), os.environ['TCP_PORT']),
                   'api_key': config.secrets()['PDNS_API_KEY'], 'server_id': 'localhost'},
        'zones': core.zone_names(pdns, ns.settings(values)),
    }


# --- lifecycle --------------------------------------------------------------

def generate_secrets():
    if not config.secrets().get('PDNS_API_KEY'):
        config.write_secrets({'PDNS_API_KEY': pysecrets.token_urlsafe(32)})


def mark_copy():
    """Clone, move and restore: the copy has the primary's zones and API key (DESIGN 10)."""
    values = config.env()
    config.set_copy_pending(True)
    if values.get('POWERDNS_ROLE') == 'primary':
        config.set_standby(True)


def keep_clone_stopped_if_blocked():
    """The core starts what the source had enabled. Leave the server to reconcile."""
    if not ns.start_blocked():
        return
    listing = config.path('default-target.clone-module')
    with open(listing) as fp:
        units = fp.read().split()
    with open(listing, 'w') as fp:
        fp.write(' '.join(u for u in units if u != ns.UNIT) + '\n')


def destroy():
    values = config.env()
    role = values.get('POWERDNS_ROLE')
    if role == 'secondary':
        ns.unregister_from_primary()
    elif role == 'primary' and not config.is_standby():
        ns.unregister_service()
        rdb = ns.redis()
        uuids = rdb.hgetall('cluster/module_uuid')
        mine = os.environ.get('MODULE_UUID')
        moving = any(k != os.environ['MODULE_ID'] and v == mine for k, v in uuids.items())
        if not moving:
            # In a move the copy registers itself in a moment and announces it.
            ns.publish('powerdns-provider-changed')
    try:
        agent.remove_public_service(os.environ['MODULE_ID'])
    except Exception as e:
        ns.log('cannot remove the firewall service: %s' % e, agent.SD_WARNING)


def restore_configure_data():
    """Every variable 06copyenv restored, mapped to configure-module's input."""
    values = config.env()
    data = {
        'role': values['POWERDNS_ROLE'],
        'ns_name': values.get('NS_NAME', ''),
        'advertise': values.get('ADVERTISE', 'true') == 'true',
        'hostmaster': values.get('HOSTMASTER', ''),
    }
    timers = config.soa_timers(values)
    for key, value in timers.items():
        data['soa_' + key] = value
    # The restore may be on another node: keep only addresses that exist here.
    available = ns.node_addresses()
    data['listen_addresses'] = [a for a in config.listen_addresses(values) if a in available]
    if values['POWERDNS_ROLE'] == 'secondary':
        primaries = ns.primaries(ns.redis())
        wanted = values.get('PRIMARY_MODULE_UUID')
        match = next((p for p in primaries if p.get('module_uuid') == wanted), primaries[0] if primaries else None)
        agent.assert_exp(match is not None, 'no primary to follow: restore the primary first')
        data['primary'] = match['module_uuid']
    return data


ACTIONS = {
    'get-configuration': get_configuration,
    'list-zones': list_zones,
    'add-zone': add_zone,
    'update-zone': update_zone,
    'remove-zone': remove_zone,
    'get-zone': get_zone,
    'check-zone-ds': check_zone_ds,
    'get-records': get_records,
    'set-records': set_records,
    'delete-records': delete_records,
    'register-secondary': register_secondary,
    'unregister-secondary': unregister_secondary,
    'list-secondaries': list_secondaries,
    'remove-secondary': remove_secondary,
    'get-dns-status': get_dns_status,
    'get-provider-config': get_provider_config,
}


def fail_validation(error):
    agent.set_status('validation-failed')
    json.dump([error.entry()], fp=sys.stdout)
    sys.exit(3)


def run_step(function, emit=True):
    """Read the request, run the step, print its output; refusals are validation failures."""
    raw = sys.stdin.read().strip()
    run_with(function, json.loads(raw) if raw else {}, emit)


def run_with(function, request, emit=False):
    try:
        output = function(request)
    except core.ActionError as e:
        fail_validation(e)
    except ApiError as e:
        print(agent.SD_ERR + 'powerdns: %s' % e, file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        # PowerDNS is not answering: stopped, or a copy waiting for its original
        print(agent.SD_WARNING + 'powerdns: %s' % e, file=sys.stderr)
        fail_validation(core.ActionError('role', 'service_unavailable', os.environ['MODULE_ID']))
    if emit:
        json.dump(output if output is not None else {}, fp=sys.stdout)


def run(action):
    run_step(ACTIONS[action])
