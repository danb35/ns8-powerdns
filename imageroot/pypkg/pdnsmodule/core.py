#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""Zones, records, DNSSEC and replication, on top of a PowerDNS API client.

Nothing here touches the node. What these functions need from the instance
comes in through a Settings object, so tests drive them against a real PowerDNS.
"""

import base64
import binascii
import ipaddress
import os

from . import config, dnsutil
from .pdnsapi import ApiError


class ActionError(Exception):
    """A refusal the administrator can act on; becomes an NS8 validation failure."""

    def __init__(self, parameter, code, value='', message=''):
        super().__init__(message or code)
        self.parameter = parameter
        self.code = code
        self.value = value
        self.message = message

    def entry(self):
        item = {'field': self.parameter, 'parameter': self.parameter, 'value': self.value, 'error': self.code}
        if self.message:
            item['message'] = self.message
        return item


class Settings:
    def __init__(self, module_id, ns_name, advertise=True, hostmaster='', soa=None, catalog='',
                 addresses=None, peers_file=None):
        self.module_id = module_id
        self.ns_name = ns_name
        self.advertise = advertise
        self.hostmaster = hostmaster
        self.soa = soa or dict(config.SOA_DEFAULTS)
        self.catalog = catalog
        self.addresses = addresses or []
        self.peers_file = peers_file


# --- peers (DESIGN 6.5, 6.6) ------------------------------------------------

def load_peers(settings):
    return config.read_json(settings.peers_file, {'peers': []})['peers']


def save_peers(settings, peers):
    config.write_json(settings.peers_file, {'peers': peers})


def internal_peers(settings):
    """Peers that are secondaries in this cluster. Unknown kinds are kept but ignored."""
    return [p for p in load_peers(settings) if p.get('kind') == 'internal']


def external_peers(settings):
    """Secondaries outside the cluster, entered by hand (DESIGN 6.6)."""
    return [p for p in load_peers(settings) if p.get('kind') == 'external']


def peer_gets_zone(peer, zone):
    """Whether an external peer is given a zone: all of them, or the ones listed."""
    if peer.get('zones') == 'all':
        return True
    return dnsutil.canonical(zone) in {dnsutil.canonical(z) for z in peer.get('zones') or []}


def _unique(items):
    return list(dict.fromkeys(items))


def tsig_key_name(secondary_module_id):
    return 'powerdns-%s' % secondary_module_id


def _key_id(name):
    return dnsutil.canonical(name)


def ns_names(settings, zone=None):
    """The apex NS of a zone: advertised instances, plus advertised external peers given the zone."""
    names = [settings.ns_name] if settings.advertise else []
    names += [p['ns_name'] for p in internal_peers(settings) if p.get('advertise') and p.get('ns_name')]
    if zone is not None:
        names += [n for p in external_peers(settings) if p.get('advertise') and peer_gets_zone(p, zone)
                  for n in p.get('ns_names', [])]
    # A zone must have an NS RRset, even when no instance is advertised.
    return sorted({dnsutil.canonical(n) for n in names}) or [dnsutil.canonical(settings.ns_name)]


def _ns_rrset(settings, zone):
    return {'name': zone, 'type': 'NS', 'ttl': 3600, 'changetype': 'REPLACE',
            'records': [{'content': n, 'disabled': False} for n in ns_names(settings, zone)]}


def _soa_content(settings, soa, serial=0):
    timers = dict(settings.soa)
    timers.update({k: v for k, v in (soa or {}).items() if v})
    return '%s %s %d %d %d %d %d' % (
        dnsutil.canonical(settings.ns_name), dnsutil.soa_rname(settings.hostmaster), serial,
        timers['refresh'], timers['retry'], timers['expire'], timers['minimum'])


def apply_peers_to_zone(pdns, settings, zone):
    """Allow each peer to transfer the zone and notify each peer of changes.

    External peers are applied to the zones they are given, and never to the catalog,
    which would tell them every zone hosted here (DESIGN 6.6).
    """
    internal = [p for p in internal_peers(settings) if p.get('catalog', True)]
    external = []
    if dnsutil.canonical(zone) != dnsutil.canonical(settings.catalog or '.'):
        external = [p for p in external_peers(settings) if peer_gets_zone(p, zone)]
    keys = [p['tsig_key'] for p in internal] + [p['tsig_key'] for p in external if p.get('auth') == 'tsig']
    pdns.update_zone(zone, {'master_tsig_key_ids': _unique(_key_id(k) for k in keys)})
    pdns.set_metadata(zone, 'ALSO-NOTIFY', _unique([p['address'] for p in internal] +
                                                   [a for p in external for a in p.get('notify', [])]))
    pdns.set_metadata(zone, 'ALLOW-AXFR-FROM', _unique(n for p in external if p.get('auth') == 'ip'
                                                       for n in p.get('transfer_from', [])))


# --- catalog (DESIGN 6.1) ---------------------------------------------------

def catalog_name(module_uuid):
    return 'catalog.%s.invalid.' % module_uuid


def ensure_catalog(pdns, settings):
    """Create the producer zone.

    PowerDNS raises a producer's serial to the current epoch time when a member
    changes, so the initial serial must be below that (see its catalog zone
    documentation). A date-style serial such as 2026110501 is above it, and the
    consumers would then never see an update; hence no SOA-EDIT-API and serial 1.
    """
    if pdns.zone_or_none(settings.catalog) is None:
        pdns.create_zone({
            'name': settings.catalog, 'kind': 'Producer', 'nameservers': ['invalid.'], 'soa_edit_api': '',
            'rrsets': [{'name': settings.catalog, 'type': 'SOA', 'ttl': 3600, 'changetype': 'REPLACE', 'records': [
                {'content': 'invalid. hostmaster.invalid. 1 3600 600 604800 1800', 'disabled': False}]}],
        })
    apply_peers_to_zone(pdns, settings, settings.catalog)


# PowerDNS renews signatures weekly but leaves the serial alone, so the secondaries
# of a signed zone that does not change would keep their copy until its signatures
# expired, three weeks later (DESIGN 7.3). INCEPTION-INCREMENT raises the served
# serial at the start of each signing week. INCEPTION-EPOCH would not: it never
# lowers a serial, and date-style serials are above the epoch time.
SOA_EDIT = 'INCEPTION-INCREMENT'


def served_serial(zone_info):
    """The serial PowerDNS answers with, after SOA-EDIT: what secondaries hold."""
    return zone_info.get('edited_serial') or zone_info.get('serial', 0)


def ensure_soa_edit(pdns, settings):
    """Give SOA_EDIT to member zones created before it was set. Returns their names."""
    fixed = []
    for info in member_zones(pdns, settings):
        if pdns.zone(info['name'], rrsets=False).get('soa_edit') != SOA_EDIT:
            pdns.update_zone(info['name'], {'soa_edit': SOA_EDIT})
            fixed.append(dnsutil.display(info['name']))
    return fixed


def is_member_zone(zone_info, settings):
    return zone_info['name'] != settings.catalog and zone_info['kind'].lower() in ('master', 'primary', 'native')


def member_zones(pdns, settings):
    return [z for z in pdns.zones() if is_member_zone(z, settings)]


def zone_names(pdns, settings):
    return sorted(dnsutil.display(z['name']) for z in member_zones(pdns, settings))


# --- zones (DESIGN 5, 7) ----------------------------------------------------

def glue_warnings(settings, zone):
    """Which NS names lie inside the zone, and the addresses the registrar needs."""
    return [{'ns_name': n['ns_name'], 'addresses': [a['address'] for a in n['addresses']]}
            for n in name_servers(settings, zone) if n['glue']]


def name_servers(settings, zone):
    """What the registrar needs for each NS name: whether it is inside the zone, and its addresses.

    An external secondary's name (DESIGN 6.6) is marked external: its addresses are the
    provider's, which the module does not know, so a name inside the zone still needs glue
    but the administrator gets the addresses from the provider.
    """
    zone = dnsutil.canonical(zone)
    known = {dnsutil.canonical(settings.ns_name): settings.addresses}
    for peer in internal_peers(settings):
        if peer.get('ns_name'):
            known[dnsutil.canonical(peer['ns_name'])] = peer.get('addresses', [])
    external = {dnsutil.canonical(n) for p in external_peers(settings) if p.get('advertise') and peer_gets_zone(p, zone)
                for n in p.get('ns_names', [])}
    return [{'ns_name': dnsutil.display(n), 'glue': dnsutil.is_subdomain(n, zone),
             'external': n in external and n not in known,
             'addresses': [{'address': a, 'public': dnsutil.is_public(a)} for a in known.get(n, [])]}
            for n in ns_names(settings, zone)]


def _same_ds(ours, theirs):
    """A parent DS matches when it has our key tag and algorithm, and our digest for SHA-256."""
    a, b = ours.split(), theirs.split()
    if a[:2] != b[:2]:
        return False
    return b[2] != '2' or a[3].upper() == b[3].upper()


def compare_delegation(zone, servers, ds_expected, observed, ds_published, resolution):
    """Compare what the zone needs at the registrar with what the parent publishes (DESIGN 7.2).

    servers: name_servers(); ds_expected: ds_records(), empty for an unsigned zone;
    observed: dnsutil.delegation() or None; ds_published: dnsutil.ds_at_parent() or None;
    resolution: dnsutil.resolver_status().
    """
    expected = [dnsutil.canonical(s['ns_name']) for s in servers]
    result = {'zone': dnsutil.display(zone), 'parent': '', 'parent_server': '', 'delegated': None,
              'ns_expected': [dnsutil.display(n) for n in expected], 'ns_published': None,
              'ns_missing': [], 'ns_extra': [], 'glue': [], 'signed': bool(ds_expected),
              'ds_expected': ds_expected, 'ds_published': ds_published, 'ds_ok': None,
              'resolution': resolution}
    if observed is not None:
        published = observed['name_servers']
        result.update({
            'parent': dnsutil.display(observed['parent']), 'parent_server': dnsutil.display(observed['server']),
            'delegated': bool(published), 'ns_published': [dnsutil.display(n) for n in published],
            'ns_missing': [dnsutil.display(n) for n in expected if n not in published],
            'ns_extra': [dnsutil.display(n) for n in published if n not in expected],
        })
        for server in servers:
            if not server['glue']:
                continue
            wanted = sorted(a['address'] for a in server['addresses'] if a['public'])
            have = sorted(observed['glue'].get(dnsutil.canonical(server['ns_name']), []))
            if server.get('external'):
                # The provider's addresses are not known here: glue being there is all that can be checked.
                ok = bool(have)
            else:
                ok = bool(have) and set(_canonical_ip(a) for a in have) == set(_canonical_ip(a) for a in wanted)
            result['glue'].append({'ns_name': server['ns_name'], 'expected': wanted, 'published': have,
                                   'external': bool(server.get('external')), 'ok': ok})
    if ds_published is not None:
        if ds_expected:
            # Every DS at the parent must match a key, or validating resolvers fail the zone
            result['ds_ok'] = bool(ds_published) and all(any(_same_ds(o, t) for o in ds_expected) for t in ds_published)
        else:
            # An unsigned zone must have no DS at all
            result['ds_ok'] = not ds_published
    return result


def _canonical_ip(address):
    return str(ipaddress.ip_address(address))


def _apply_dnssec(pdns, zone, dnssec, denial):
    body = {'dnssec': bool(dnssec)}
    if dnssec:
        # RFC 9276: no opt-out, no extra iterations, no salt. Never narrow: a
        # narrow zone refuses AXFR, which would break secondaries.
        body['nsec3param'] = '1 0 0 -' if denial == 'nsec3' else ''
        body['nsec3narrow'] = False
    pdns.update_zone(zone, body)


def add_zone(pdns, settings, name, dnssec=False, denial='nsec3', soa=None):
    if not dnsutil.is_dns_name(name):
        raise ActionError('zone', 'invalid_zone_name', name)
    zone = dnsutil.canonical(name)
    if pdns.zone_or_none(zone) is not None:
        raise ActionError('zone', 'zone_exists', name)
    pdns.create_zone({
        'name': zone,
        'kind': 'Primary',
        'soa_edit_api': 'DEFAULT',
        'soa_edit': SOA_EDIT,
        'api_rectify': True,
        'catalog': settings.catalog,
        'rrsets': [
            {'name': zone, 'type': 'SOA', 'ttl': 3600, 'changetype': 'REPLACE',
             'records': [{'content': _soa_content(settings, soa), 'disabled': False}]},
            _ns_rrset(settings, zone),
        ],
    })
    apply_peers_to_zone(pdns, settings, zone)
    if dnssec:
        _apply_dnssec(pdns, zone, True, denial)
    return {'zone': dnsutil.display(zone), 'glue': glue_warnings(settings, zone)}


def update_zone(pdns, settings, name, dnssec=None, denial=None, soa=None):
    zone = _existing_zone(pdns, name)
    if soa:
        info = pdns.zone(zone)
        current = next(r for r in info['rrsets'] if r['type'] == 'SOA')['records'][0]['content'].split()
        timers = dict(zip(('refresh', 'retry', 'expire', 'minimum'), map(int, current[3:7])))
        timers.update({k: v for k, v in soa.items() if v})
        content = ' '.join(current[:3] + [str(timers[k]) for k in ('refresh', 'retry', 'expire', 'minimum')])
        pdns.patch_rrsets(zone, [{'name': zone, 'type': 'SOA', 'ttl': 3600, 'changetype': 'REPLACE',
                                  'records': [{'content': content, 'disabled': False}]}])
    if dnssec is not None or denial is not None:
        info = pdns.zone(zone, rrsets=False)
        enabled = info['dnssec'] if dnssec is None else dnssec
        if not enabled and denial is not None and dnssec is None:
            raise ActionError('denial', 'dnssec_not_enabled', denial)
        _apply_dnssec(pdns, zone, enabled, denial or ('nsec3' if info.get('nsec3param') or not info['dnssec'] else 'nsec'))
    return get_zone(pdns, settings, zone)


def remove_zone(pdns, settings, name):
    """Delete the zone, and take it out of the external peers' lists (DESIGN 6.6)."""
    zone = _existing_zone(pdns, name)
    pdns.delete_zone(zone)
    peers = load_peers(settings)
    changed = False
    for peer in peers:
        if peer.get('kind') == 'external' and isinstance(peer.get('zones'), list):
            kept = [z for z in peer['zones'] if dnsutil.canonical(z) != zone]
            changed = changed or len(kept) != len(peer['zones'])
            peer['zones'] = kept
    if changed:
        save_peers(settings, peers)


def _existing_zone(pdns, name):
    zone = dnsutil.canonical(name)
    if pdns.zone_or_none(zone) is None:
        raise ActionError('zone', 'zone_not_found', name)
    return zone


def ds_records(pdns, zone):
    """SHA-256 digests only, the ones a registrar asks for (DESIGN 7.2)."""
    out = []
    for key in pdns.cryptokeys(zone):
        if not key.get('published', True):
            continue
        for ds in key.get('ds') or []:
            fields = ds.split()
            if len(fields) == 4 and fields[2] == '2':
                out.append(ds)
    return out


def dnskey_records(pdns, zone):
    """The published keys, for registries that take a DNSKEY instead of a DS."""
    return [key['dnskey'] for key in pdns.cryptokeys(zone) if key.get('published', True) and key.get('dnskey')]


def get_zone(pdns, settings, name):
    zone = _existing_zone(pdns, name)
    info = pdns.zone(zone, rrsets=False)
    kind = info['kind'].lower()
    primary = kind in ('master', 'primary', 'native')
    result = {
        'zone': dnsutil.display(zone),
        'kind': kind,
        'serial': served_serial(info),
        'dnssec': bool(info.get('dnssec')),
        'denial': ('nsec3' if info.get('nsec3param') else 'nsec') if info.get('dnssec') else None,
        # A secondary holds no keys, so its copy has no DS to show (DESIGN 3).
        'ds_records': ds_records(pdns, zone) if primary and info.get('dnssec') else [],
        'dnskey_records': dnskey_records(pdns, zone) if primary and info.get('dnssec') else [],
    }
    if primary:
        result['name_servers'] = name_servers(settings, zone)
    return result


def list_zones(pdns, settings):
    zones = []
    for info in pdns.zones():
        if info['name'] == settings.catalog or info['kind'].lower() in ('consumer', 'producer'):
            continue
        entry = {'zone': dnsutil.display(info['name']), 'kind': info['kind'].lower(),
                 'serial': served_serial(info), 'dnssec': bool(info.get('dnssec'))}
        if entry['kind'] in ('slave', 'secondary'):
            entry['last_check'] = info.get('last_check', 0)
            entry['transferred'] = info.get('serial', 0) != 0
        zones.append(entry)
    return sorted(zones, key=lambda z: z['zone'])


# --- records (DESIGN 8.3, 9.1) ----------------------------------------------

def get_records(pdns, name):
    zone = _existing_zone(pdns, name)
    records = []
    for rrset in pdns.zone(zone)['rrsets']:
        if rrset['type'] in ('RRSIG', 'NSEC', 'NSEC3', 'NSEC3PARAM', 'DNSKEY', 'CDS', 'CDNSKEY'):
            continue
        for record in rrset['records']:
            if not record.get('disabled'):
                records.append({
                    'name': dnsutil.relative_name(rrset['name'], zone),
                    'type': rrset['type'],
                    'ttl': rrset['ttl'],
                    'data': dnsutil.from_presentation(rrset['type'], record['content']),
                })
    return sorted(records, key=lambda r: (r['name'] != '@', r['name'], r['type'], r['data']))


def _check_writable(zone, owner, rtype, value):
    """Apex NS and SOA belong to this module; the rest of the zone may be edited."""
    if not dnsutil.is_subdomain(owner, zone):
        raise ActionError('records', 'name_outside_zone', value)
    if rtype == 'SOA' or (rtype == 'NS' and dnsutil.canonical(owner) == zone):
        raise ActionError('records', 'apex_protected', value)


def set_records(pdns, name, records):
    """Each (name, type) in the input becomes exactly the values given, atomically."""
    zone = _existing_zone(pdns, name)
    sets = {}
    for record in records:
        rtype = record['type'].upper()
        owner = dnsutil.absolute_name(record['name'], zone)
        _check_writable(zone, owner, rtype, record['name'])
        entry = sets.setdefault((owner, rtype), {'name': owner, 'type': rtype, 'ttl': 0, 'changetype': 'REPLACE', 'records': []})
        entry['ttl'] = record.get('ttl') or entry['ttl'] or 3600
        entry['records'].append({'content': dnsutil.to_presentation(rtype, record['data']), 'disabled': False})
    _patch(pdns, zone, list(sets.values()))
    return get_records(pdns, zone)


def delete_records(pdns, name, records):
    """Delete a whole RRset, or only the values listed in `data`."""
    zone = _existing_zone(pdns, name)
    current = {(r['name'], r['type']): r for r in pdns.zone(zone)['rrsets']}
    changes = {}
    for record in records:
        rtype = record['type'].upper()
        owner = dnsutil.absolute_name(record['name'], zone)
        _check_writable(zone, owner, rtype, record['name'])
        existing = changes.get((owner, rtype)) or current.get((owner, rtype))
        if existing is None:
            continue
        if record.get('data') is None:
            changes[(owner, rtype)] = {'name': owner, 'type': rtype, 'changetype': 'DELETE', 'records': []}
            continue
        drop = dnsutil.to_presentation(rtype, record['data'])
        left = [r for r in existing['records'] if r['content'] != drop]
        if left:
            changes[(owner, rtype)] = {'name': owner, 'type': rtype, 'ttl': existing.get('ttl', 3600),
                                       'changetype': 'REPLACE', 'records': left}
        else:
            changes[(owner, rtype)] = {'name': owner, 'type': rtype, 'changetype': 'DELETE', 'records': []}
    _patch(pdns, zone, list(changes.values()))
    return get_records(pdns, zone)


def _patch(pdns, zone, rrsets):
    if not rrsets:
        return
    try:
        pdns.patch_rrsets(zone, rrsets)
    except ApiError as e:
        if e.status in (400, 422):
            raise ActionError('records', 'invalid_record', '', e.message) from None
        raise


# --- replication, primary side (DESIGN 6.2) ---------------------------------

def rewrite_apex_ns(pdns, settings):
    for info in member_zones(pdns, settings):
        pdns.patch_rrsets(info['name'], [_ns_rrset(settings, info['name'])])


def apply_peers_everywhere(pdns, settings):
    ensure_catalog(pdns, settings)
    for info in member_zones(pdns, settings):
        apply_peers_to_zone(pdns, settings, info['name'])


def register_secondary(pdns, settings, module_id, address, ns_name, advertise, addresses=None):
    """Add or refresh a peer. Registering again returns the same key."""
    key_name = tsig_key_name(module_id)
    key = pdns.tsigkey(_key_id(key_name)) or pdns.create_tsigkey(key_name)
    peers = [p for p in load_peers(settings) if p.get('id') != module_id]
    peers.append({'id': module_id, 'kind': 'internal', 'address': address, 'tsig_key': key_name,
                  'ns_name': ns_name, 'advertise': bool(advertise), 'catalog': True,
                  'addresses': addresses or []})
    save_peers(settings, peers)
    apply_peers_everywhere(pdns, settings)
    rewrite_apex_ns(pdns, settings)
    return {'tsig_key': key_name, 'tsig_secret': key['key'], 'algorithm': 'hmac-sha256',
            'catalog': settings.catalog}


def unregister_secondary(pdns, settings, module_id):
    """Forget a peer and revoke its key. Forgetting an unknown peer is not an error."""
    peers = load_peers(settings)
    remaining = [p for p in peers if p.get('id') != module_id]
    save_peers(settings, remaining)
    if len(remaining) != len(peers):
        apply_peers_everywhere(pdns, settings)
        rewrite_apex_ns(pdns, settings)
    pdns.delete_tsigkey(_key_id(tsig_key_name(module_id)))


def secondaries_status(pdns, settings, query_serial=dnsutil.soa_serial):
    """Each peer with how many member zones it serves at the primary's serial.

    A peer is reachable when it answers for the catalog, which every secondary holds, or for any
    member zone; with no member zones the catalog alone decides.
    """
    zones = [(z['name'], served_serial(z), z.get('notified_serial', 0)) for z in member_zones(pdns, settings)]
    out = []
    for peer in load_peers(settings):
        if peer.get('kind') != 'internal':
            continue
        reachable = settings.catalog and query_serial(peer['address'], settings.catalog) is not None
        behind = []
        for name, serial, _notified in zones:
            theirs = query_serial(peer['address'], name)
            if theirs is None:
                behind.append(dnsutil.display(name))
            else:
                reachable = True
                if theirs != serial:
                    behind.append(dnsutil.display(name))
        reachable = bool(reachable)
        out.append({'module_id': peer['id'], 'address': peer['address'], 'ns_name': peer.get('ns_name', ''),
                    'advertise': bool(peer.get('advertise')), 'reachable': reachable,
                    'zones_total': len(zones), 'zones_behind': behind})
    return sorted(out, key=lambda p: p['module_id'])


# --- external secondaries (DESIGN 6.6) -------------------------------------

# Secret sizes follow each algorithm's digest length (RFC 2104 recommends no less).
TSIG_ALGORITHMS = {'hmac-md5': 16, 'hmac-sha1': 20, 'hmac-sha224': 28, 'hmac-sha256': 32,
                   'hmac-sha384': 48, 'hmac-sha512': 64}
# The narrowest network an IP-only peer may name: a typo must not open a zone to
# a large part of the internet.
MIN_PREFIX = {4: 24, 6: 48}


def generate_tsig_secret(algorithm):
    return base64.b64encode(os.urandom(TSIG_ALGORITHMS[algorithm])).decode()


def _check_secret(secret):
    try:
        if base64.b64decode(secret, validate=True):
            return
    except (binascii.Error, ValueError):
        pass
    raise ActionError('tsig_secret', 'invalid_tsig_secret', '')


def _network(entry):
    try:
        net = ipaddress.ip_network(entry.strip(), strict=False)
    except ValueError:
        raise ActionError('transfer_from', 'invalid_network', entry) from None
    if net.prefixlen < MIN_PREFIX[net.version]:
        raise ActionError('transfer_from', 'network_too_wide', entry)
    return str(net)


def normalize_external(request, peers, member_zones_names, peer_id=None):
    """Check an add or update request and return the peer record it describes, without its key.

    Pure, so the rules are tested without PowerDNS. member_zones_names: the zones the primary
    hosts, canonical. peer_id: the peer being updated, None for a new one.
    """
    others = [p for p in peers if p.get('kind') == 'external' and p.get('id') != peer_id]
    name = (request.get('name') or '').strip()
    if not name:
        raise ActionError('name', 'name_required', '')
    if any(p.get('name', '').lower() == name.lower() for p in others):
        raise ActionError('name', 'name_exists', name)
    notify = _unique(a.strip() for a in request.get('notify') or [] if a.strip())
    if not notify:
        raise ActionError('notify', 'notify_required', '')
    for address in notify:
        if not dnsutil.is_ip(address):
            raise ActionError('notify', 'invalid_address', address)
    notify = [str(ipaddress.ip_address(a)) for a in notify]
    auth = request.get('auth', 'tsig')
    transfer_from = []
    if auth == 'ip':
        transfer_from = _unique(_network(e) for e in request.get('transfer_from') or [] if e.strip())
        if not transfer_from:
            raise ActionError('transfer_from', 'transfer_from_required', '')
    ns = []
    for n in request.get('ns_names') or []:
        if not n.strip():
            continue
        if not dnsutil.is_dns_name(n.strip()):
            raise ActionError('ns_names', 'invalid_ns_name', n)
        ns.append(dnsutil.canonical(n.strip()).rstrip('.'))
    zones = request.get('zones', 'all')
    if zones != 'all':
        listed = []
        for z in zones or []:
            if dnsutil.canonical(z) not in member_zones_names:
                raise ActionError('zones', 'zone_not_found', z)
            listed.append(dnsutil.display(dnsutil.canonical(z)))
        zones = sorted(set(listed))
    if peer_id is None:
        used = {int(p['id'][3:]) for p in peers if p.get('kind') == 'external' and p.get('id', '')[3:].isdigit()}
        peer_id = 'ext%d' % next(i for i in range(1, len(used) + 2) if i not in used)
    return {'id': peer_id, 'kind': 'external', 'name': name, 'notify': notify, 'auth': auth,
            'transfer_from': transfer_from, 'ns_names': _unique(ns), 'advertise': bool(request.get('advertise', True)),
            'zones': zones}


def _tsig_request(request):
    """The key part of a request: algorithm, key name and pasted secret, each optional."""
    tsig = request.get('tsig') or {}
    algorithm = tsig.get('algorithm') or 'hmac-sha256'
    if algorithm not in TSIG_ALGORITHMS:
        raise ActionError('tsig_algorithm', 'invalid_tsig_algorithm', algorithm)
    key_name = (tsig.get('key_name') or '').strip()
    if key_name and not dnsutil.is_key_name(key_name):
        raise ActionError('tsig_key_name', 'invalid_tsig_key_name', key_name)
    secret = (tsig.get('secret') or '').strip()
    if secret:
        _check_secret(secret)
    return algorithm, key_name.rstrip('.'), secret


def _install_key(pdns, peers, peer, key_name, algorithm, secret, current=None):
    """Create the peer's key, refusing a name another peer or an unrelated key holds."""
    key_name = key_name or 'powerdns-%s' % peer['id']
    if key_name != current:
        taken = {p.get('tsig_key') for p in peers if p.get('id') != peer['id']}
        if key_name in taken or pdns.tsigkey(_key_id(key_name)) is not None:
            raise ActionError('tsig_key_name', 'tsig_key_exists', key_name)
    else:
        pdns.delete_tsigkey(_key_id(key_name))
    pdns.create_tsigkey(key_name, secret or generate_tsig_secret(algorithm), algorithm)
    peer['tsig_key'] = key_name


def _external_view(peer):
    keys = ('id', 'name', 'notify', 'auth', 'tsig_key', 'transfer_from', 'ns_names', 'advertise', 'zones')
    out = {k: peer.get(k) for k in keys}
    out['tsig_key'] = out['tsig_key'] or ''
    return out


def _member_names(pdns, settings):
    return {dnsutil.canonical(z['name']) for z in member_zones(pdns, settings)}


def _reapply(pdns, settings):
    apply_peers_everywhere(pdns, settings)
    rewrite_apex_ns(pdns, settings)


def add_external_secondary(pdns, settings, request):
    peers = load_peers(settings)
    peer = normalize_external(request, peers, _member_names(pdns, settings))
    if peer['auth'] == 'tsig':
        algorithm, key_name, secret = _tsig_request(request)
        _install_key(pdns, peers, peer, key_name, algorithm, secret)
    save_peers(settings, peers + [peer])
    _reapply(pdns, settings)
    out = {'secondary': _external_view(peer)}
    if peer['auth'] == 'tsig':
        out['key'] = external_secondary_key(pdns, settings, peer['id'])
    return out


def _external(peers, peer_id):
    for peer in peers:
        if peer.get('kind') == 'external' and peer.get('id') == peer_id:
            return peer
    raise ActionError('id', 'external_not_found', peer_id)


def update_external_secondary(pdns, settings, request):
    """Change a peer; fields left out keep their value.

    A new key is made when the request pastes a secret or asks for one (tsig.regenerate), changes
    the algorithm or the key name, or moves the peer to TSIG; the old key is revoked once the zones
    no longer name it. Moving to IP-only revokes the key.
    """
    peers = load_peers(settings)
    old = _external(peers, request['id'])
    merged = {k: old.get(k) for k in ('name', 'notify', 'auth', 'transfer_from', 'ns_names', 'advertise', 'zones')}
    merged.update({k: v for k, v in request.items() if k not in ('id', 'tsig')})
    peer = normalize_external(merged, peers, _member_names(pdns, settings), peer_id=old['id'])
    old_key = old.get('tsig_key') or ''
    new_key = False
    if peer['auth'] == 'tsig':
        tsig = request.get('tsig') or {}
        algorithm, key_name, secret = _tsig_request(request)
        key_name = key_name or old_key
        current = pdns.tsigkey(_key_id(old_key)) if old_key and old.get('auth') == 'tsig' else None
        current_algorithm = (current or {}).get('algorithm', '').rstrip('.')
        new_key = bool(current is None or secret or tsig.get('regenerate') or key_name != old_key
                       or (tsig.get('algorithm') and algorithm != current_algorithm))
        if new_key:
            _install_key(pdns, peers, peer, key_name, algorithm, secret,
                         current=old_key if current is not None else None)
        else:
            peer['tsig_key'] = old_key
    save_peers(settings, [peer if p is old else p for p in peers])
    _reapply(pdns, settings)
    if old_key and old_key != peer.get('tsig_key'):
        pdns.delete_tsigkey(_key_id(old_key))
    out = {'secondary': _external_view(peer)}
    if new_key:
        out['key'] = external_secondary_key(pdns, settings, peer['id'])
    return out


def remove_external_secondary(pdns, settings, peer_id):
    peers = load_peers(settings)
    peer = _external(peers, peer_id)
    save_peers(settings, [p for p in peers if p is not peer])
    _reapply(pdns, settings)
    if peer.get('tsig_key'):
        pdns.delete_tsigkey(_key_id(peer['tsig_key']))


def external_secondary_key(pdns, settings, peer_id):
    """The TSIG key to give the provider."""
    peer = _external(load_peers(settings), peer_id)
    if peer.get('auth') != 'tsig' or not peer.get('tsig_key'):
        raise ActionError('id', 'no_tsig_key', peer_id)
    key = pdns.tsigkey(_key_id(peer['tsig_key']))
    if key is None:
        raise ActionError('id', 'no_tsig_key', peer_id)
    return {'key_name': peer['tsig_key'], 'algorithm': key['algorithm'].rstrip('.'), 'secret': key['key']}


def external_status(pdns, settings, query_serial=dnsutil.soa_serial):
    """Each external peer, with the given zones whose serial at its notify addresses differs."""
    zones = [(z['name'], served_serial(z)) for z in member_zones(pdns, settings)]
    out = []
    for peer in external_peers(settings):
        given = [(n, s) for n, s in zones if peer_gets_zone(peer, n)]
        answering = False
        behind = []
        for name, serial in given:
            theirs = None
            for address in peer.get('notify', []):
                theirs = query_serial(address, name)
                if theirs is not None:
                    break
            if theirs is None:
                behind.append(dnsutil.display(name))
            else:
                answering = True
                if theirs != serial:
                    behind.append(dnsutil.display(name))
        view = _external_view(peer)
        view.update({'answering': answering, 'zones_total': len(given), 'zones_behind': behind})
        out.append(view)
    return sorted(out, key=lambda p: p['name'].lower())


# --- replication, secondary side (DESIGN 6.2, 7.3) --------------------------

def ensure_consumer(pdns, catalog, primary_address, key_name, key_secret):
    """Install the key and the consumer zone, and make an existing one follow them."""
    key_id = _key_id(key_name)
    existing = pdns.tsigkey(key_id)
    if existing is not None and existing.get('key') != key_secret:
        pdns.delete_tsigkey(key_id)
        existing = None
    if existing is None:
        pdns.create_tsigkey(key_name, key_secret)
    zone = pdns.zone_or_none(catalog)
    if zone is None:
        pdns.create_zone({'name': catalog, 'kind': 'Consumer', 'masters': [primary_address],
                          'slave_tsig_key_ids': [key_id]})
    else:
        pdns.update_zone(catalog, {'masters': [primary_address], 'slave_tsig_key_ids': [key_id]})
    pdns.retrieve(catalog)


def reconcile_members(pdns, catalog, primary_address, key_name):
    """Give catalog members what they do not get by themselves.

    Tested against 5.0.8: a member created from a catalog takes the consumer's
    primaries but NOT its AXFR-MASTER-TSIG, so its first transfer is refused. A
    refused zone also backs off, hence the explicit retrieval. PRESIGNED needs
    nothing: PowerDNS sets it when a transfer brings signatures.
    """
    key_id = _key_id(key_name)
    fixed = []
    for info in pdns.zones():
        if info['kind'].lower() not in ('slave', 'secondary') or info.get('catalog') != catalog:
            continue
        zone = pdns.zone(info['name'], rrsets=False)
        changes = {}
        if zone.get('slave_tsig_key_ids') != [key_id]:
            changes['slave_tsig_key_ids'] = [key_id]
        if zone.get('masters') != [primary_address]:
            changes['masters'] = [primary_address]
        if changes:
            pdns.update_zone(info['name'], changes)
        if changes or not zone.get('serial'):
            pdns.retrieve(info['name'])
            fixed.append(dnsutil.display(info['name']))
    return fixed


def secondary_zones_status(pdns, primary_address, query_serial=dnsutil.soa_serial):
    out = []
    for info in pdns.zones():
        if info['kind'].lower() not in ('slave', 'secondary'):
            continue
        out.append({'zone': dnsutil.display(info['name']), 'serial': info.get('serial', 0),
                    'primary_serial': query_serial(primary_address, info['name']) if primary_address else None})
    return sorted(out, key=lambda z: z['zone'])
