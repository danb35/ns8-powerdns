#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""Zones, records, DNSSEC and replication, on top of a PowerDNS API client.

Nothing here touches the node. What these functions need from the instance
comes in through a Settings object, so tests drive them against a real PowerDNS.
"""

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


# --- peers (DESIGN 6.5) -----------------------------------------------------

def load_peers(settings):
    return config.read_json(settings.peers_file, {'peers': []})['peers']


def save_peers(settings, peers):
    config.write_json(settings.peers_file, {'peers': peers})


def internal_peers(settings):
    """v1 acts only on internal peers; unknown kinds are kept but ignored."""
    return [p for p in load_peers(settings) if p.get('kind') == 'internal']


def tsig_key_name(secondary_module_id):
    return 'powerdns-%s' % secondary_module_id


def _key_id(name):
    return dnsutil.canonical(name)


def ns_names(settings):
    names = [settings.ns_name] if settings.advertise else []
    names += [p['ns_name'] for p in internal_peers(settings) if p.get('advertise') and p.get('ns_name')]
    # A zone must have an NS RRset, even when no instance is advertised.
    return sorted({dnsutil.canonical(n) for n in names}) or [dnsutil.canonical(settings.ns_name)]


def _ns_rrset(settings, zone):
    return {'name': zone, 'type': 'NS', 'ttl': 3600, 'changetype': 'REPLACE',
            'records': [{'content': n, 'disabled': False} for n in ns_names(settings)]}


def _soa_content(settings, soa, serial=0):
    timers = dict(settings.soa)
    timers.update({k: v for k, v in (soa or {}).items() if v})
    return '%s %s %d %d %d %d %d' % (
        dnsutil.canonical(settings.ns_name), dnsutil.soa_rname(settings.hostmaster), serial,
        timers['refresh'], timers['retry'], timers['expire'], timers['minimum'])


def apply_peers_to_zone(pdns, settings, zone):
    """Allow each peer's key to transfer the zone and notify each peer of changes."""
    peers = [p for p in internal_peers(settings) if p.get('catalog', True)]
    pdns.update_zone(zone, {'master_tsig_key_ids': [_key_id(p['tsig_key']) for p in peers]})
    pdns.set_metadata(zone, 'ALSO-NOTIFY', [p['address'] for p in peers])


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


def is_member_zone(zone_info, settings):
    return zone_info['name'] != settings.catalog and zone_info['kind'].lower() in ('master', 'primary', 'native')


def member_zones(pdns, settings):
    return [z for z in pdns.zones() if is_member_zone(z, settings)]


def zone_names(pdns, settings):
    return sorted(dnsutil.display(z['name']) for z in member_zones(pdns, settings))


# --- zones (DESIGN 5, 7) ----------------------------------------------------

def glue_warnings(settings, zone):
    """Which NS names lie inside the zone, and the addresses the registrar needs."""
    zone = dnsutil.canonical(zone)
    known = {dnsutil.canonical(settings.ns_name): settings.addresses}
    for peer in internal_peers(settings):
        if peer.get('ns_name'):
            known[dnsutil.canonical(peer['ns_name'])] = peer.get('addresses', [])
    return [{'ns_name': dnsutil.display(n), 'addresses': known.get(n, [])}
            for n in ns_names(settings) if dnsutil.is_subdomain(n, zone)]


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
    peers = [p for p in internal_peers(settings) if p.get('catalog', True)]
    pdns.create_zone({
        'name': zone,
        'kind': 'Primary',
        'soa_edit_api': 'DEFAULT',
        'api_rectify': True,
        'catalog': settings.catalog,
        'master_tsig_key_ids': [_key_id(p['tsig_key']) for p in peers],
        'rrsets': [
            {'name': zone, 'type': 'SOA', 'ttl': 3600, 'changetype': 'REPLACE',
             'records': [{'content': _soa_content(settings, soa), 'disabled': False}]},
            _ns_rrset(settings, zone),
        ],
    })
    pdns.set_metadata(zone, 'ALSO-NOTIFY', [p['address'] for p in peers])
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


def remove_zone(pdns, name):
    zone = _existing_zone(pdns, name)
    pdns.delete_zone(zone)


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


def get_zone(pdns, settings, name):
    zone = _existing_zone(pdns, name)
    info = pdns.zone(zone, rrsets=False)
    kind = info['kind'].lower()
    primary = kind in ('master', 'primary', 'native')
    result = {
        'zone': dnsutil.display(zone),
        'kind': kind,
        'serial': info.get('serial', 0),
        'dnssec': bool(info.get('dnssec')),
        'denial': ('nsec3' if info.get('nsec3param') else 'nsec') if info.get('dnssec') else None,
        # A secondary holds no keys, so its copy has no DS to show (DESIGN 3).
        'ds_records': ds_records(pdns, zone) if primary and info.get('dnssec') else [],
    }
    if primary:
        result['glue'] = glue_warnings(settings, zone)
    return result


def list_zones(pdns, settings):
    zones = []
    for info in pdns.zones():
        if info['name'] == settings.catalog or info['kind'].lower() in ('consumer', 'producer'):
            continue
        entry = {'zone': dnsutil.display(info['name']), 'kind': info['kind'].lower(),
                 'serial': info.get('serial', 0), 'dnssec': bool(info.get('dnssec'))}
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
    """Each peer with how many member zones it serves at the primary's serial."""
    zones = [(z['name'], z.get('serial', 0), z.get('notified_serial', 0)) for z in member_zones(pdns, settings)]
    out = []
    for peer in load_peers(settings):
        if peer.get('kind') != 'internal':
            continue
        reachable = True
        behind = []
        for name, serial, _notified in zones:
            theirs = query_serial(peer['address'], name)
            if theirs is None:
                reachable = False
                behind.append(dnsutil.display(name))
            elif theirs != serial:
                behind.append(dnsutil.display(name))
        out.append({'module_id': peer['id'], 'address': peer['address'], 'ns_name': peer.get('ns_name', ''),
                    'advertise': bool(peer.get('advertise')), 'reachable': reachable,
                    'zones_total': len(zones), 'zones_behind': behind})
    return sorted(out, key=lambda p: p['module_id'])


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
