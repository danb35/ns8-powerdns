#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""DNS names, record conversion and a minimal stub query, standard library only.

The NS8 agent environment has no DNS library, and the module needs only a SOA
serial, "does a DS record exist" and what a parent zone delegates.
"""

import ipaddress
import random
import re
import socket
import struct

_LABEL = re.compile(r'^(?!-)[A-Za-z0-9_-]{1,63}(?<!-)$')

# Types whose last field is a domain name, as in dnshelper's PowerDNS provider.
TARGET_TYPES = {'CNAME', 'DNAME', 'MX', 'NS', 'PTR', 'SRV'}
TXT_TYPES = {'TXT', 'SPF'}

QTYPE_A = 1
QTYPE_NS = 2
QTYPE_SOA = 6
QTYPE_AAAA = 28
QTYPE_DS = 43

RCODE_NOERROR = 0
RCODE_SERVFAIL = 2
RCODE_NXDOMAIN = 3


def canonical(name):
    """Lower case with a final dot: the form the PowerDNS API uses as a zone id."""
    return name.strip().lower().rstrip('.') + '.'


def display(name):
    """A name as the UI and the other modules see it: no final dot."""
    return name.rstrip('.')


def is_dns_name(name):
    """True for a syntactically valid absolute or relative name with 2+ labels."""
    stripped = name.strip().rstrip('.')
    if not stripped or len(stripped) > 253:
        return False
    labels = stripped.split('.')
    return len(labels) >= 2 and all(_LABEL.match(label) for label in labels)


def is_subdomain(name, zone):
    """True when name equals zone or lies inside it."""
    name, zone = canonical(name), canonical(zone)
    return name == zone or name.endswith('.' + zone)


def relative_name(name, zone):
    """Absolute name to dnshelper's relative form; '@' is the apex."""
    name, zone = canonical(name), canonical(zone)
    if name == zone:
        return '@'
    if name.endswith('.' + zone):
        return name[:-(len(zone) + 1)]
    return name


def absolute_name(name, zone):
    """dnshelper's relative form to an absolute name."""
    zone = canonical(zone)
    if name in ('@', ''):
        return zone
    if name.endswith('.'):
        return name.lower()
    return name.lower() + '.' + zone


def txt_quote(value):
    """Plain text to one or more quoted strings of at most 255 bytes each."""
    if not value:
        return '""'
    raw = value.encode('utf-8')
    chunks = []
    start = 0
    while start < len(raw):
        end = min(start + 255, len(raw))
        # do not cut a multi-byte character in two
        while end < len(raw) and end > start and (raw[end] & 0xC0) == 0x80:
            end -= 1
        chunks.append(raw[start:end].decode('utf-8'))
        start = end
    return ' '.join('"%s"' % c.replace('\\', '\\\\').replace('"', '\\"') for c in chunks)


def txt_unquote(content):
    """Quoted strings as PowerDNS stores them to the plain value."""
    parts = []
    i = 0
    while i < len(content):
        if content[i] != '"':
            i += 1
            continue
        i += 1
        current = []
        while i < len(content) and content[i] != '"':
            if content[i] == '\\' and i + 1 < len(content):
                i += 1
            current.append(content[i])
            i += 1
        parts.append(''.join(current))
        i += 1
    return ''.join(parts) if parts else content


def to_presentation(rtype, data):
    """dnshelper's `data` to the content PowerDNS expects."""
    rtype = rtype.upper()
    if rtype in TXT_TYPES:
        return txt_quote(data)
    if rtype in TARGET_TYPES:
        fields = data.split()
        if fields and not fields[-1].endswith('.'):
            fields[-1] += '.'
        return ' '.join(fields)
    return data


def from_presentation(rtype, content):
    """PowerDNS content to dnshelper's `data`."""
    if rtype.upper() in TXT_TYPES:
        return txt_unquote(content)
    return content


def soa_rname(hostmaster):
    """hostmaster@example.com (or already hostmaster.example.com) to a SOA RNAME."""
    hostmaster = hostmaster.strip().rstrip('.')
    if '@' in hostmaster:
        local, domain = hostmaster.split('@', 1)
        return local.replace('.', '\\.') + '.' + domain + '.'
    return hostmaster + '.'


def is_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def _encode_name(name):
    out = b''
    for label in canonical(name).rstrip('.').split('.'):
        encoded = label.encode('ascii')
        out += struct.pack('B', len(encoded)) + encoded
    return out + b'\0'


def _skip_name(buf, pos):
    while True:
        length = buf[pos]
        if length == 0:
            return pos + 1
        if length & 0xC0 == 0xC0:
            return pos + 2
        pos += length + 1


def read_name(buf, pos):
    """The name at pos, following compression pointers, in canonical form."""
    labels = []
    for _ in range(128):
        length = buf[pos]
        if length == 0:
            return '.'.join(labels).lower() + '.' if labels else '.'
        if length & 0xC0 == 0xC0:
            pos = struct.unpack('!H', buf[pos:pos + 2])[0] & 0x3FFF
            continue
        labels.append(buf[pos + 1:pos + 1 + length].decode('ascii', 'replace'))
        pos += length + 1
    raise ValueError('compression loop')


def _records(buf, pos, count):
    """count resource records from pos: [(owner, type, rdata, rdata_pos)], and the next pos."""
    out = []
    for _ in range(count):
        owner = read_name(buf, pos)
        pos = _skip_name(buf, pos)
        rtype, _klass, _ttl, rdlength = struct.unpack('!HHIH', buf[pos:pos + 10])
        pos += 10
        out.append((owner, rtype, buf[pos:pos + rdlength], pos))
        pos += rdlength
    return out, pos


def query(server, name, qtype, port=53, timeout=3.0, recursion=False):
    """One UDP query.

    Returns {'rcode', 'answers': [(type, rdata, pos)], 'authority' and 'additional':
    [(owner, type, rdata, pos)], 'raw'}. Raises OSError when the server does not answer.
    """
    qid = random.randint(0, 0xFFFF)
    flags = 0x0100 if recursion else 0
    packet = struct.pack('!HHHHHH', qid, flags, 1, 0, 0, 0) + _encode_name(name) + struct.pack('!HH', qtype, 1)
    family = socket.AF_INET6 if ':' in server else socket.AF_INET
    with socket.socket(family, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        sock.sendto(packet, (server, port))
        while True:
            buf, _ = sock.recvfrom(4096)
            if len(buf) >= 12 and struct.unpack('!H', buf[:2])[0] == qid:
                break
    rcode = buf[3] & 0x0F
    qdcount, ancount, nscount, arcount = struct.unpack('!HHHH', buf[4:12])
    pos = 12
    for _ in range(qdcount):
        pos = _skip_name(buf, pos) + 4
    sections = []
    for count in (ancount, nscount, arcount):
        try:
            records, pos = _records(buf, pos, count)
        except (IndexError, struct.error, ValueError):
            # A truncated reply: keep the sections that were read whole
            records = []
        sections.append(records)
    answers, authority, additional = sections
    return {'rcode': rcode, 'answers': [(t, d, p) for _o, t, d, p in answers],
            'answer_records': answers, 'authority': authority, 'additional': additional, 'raw': buf}


def soa_serial(server, zone, port=53, timeout=2.0):
    """The zone's serial on an authoritative server, None if it does not answer."""
    try:
        result = query(server, zone, QTYPE_SOA, port=port, timeout=timeout)
    except OSError:
        return None
    for rtype, _rdata, rdata_pos in result['answers']:
        if rtype == QTYPE_SOA:
            buf = result['raw']
            pos = _skip_name(buf, _skip_name(buf, rdata_pos))
            return struct.unpack('!I', buf[pos:pos + 4])[0]
    return None


def _address(rtype, rdata):
    family = socket.AF_INET if rtype == QTYPE_A else socket.AF_INET6
    return socket.inet_ntop(family, rdata)


def resolve_addresses(resolver, name, timeout=3.0):
    """A and AAAA of name through a resolver; [] when it has none or does not answer."""
    out = []
    for qtype in (QTYPE_A, QTYPE_AAAA):
        try:
            result = query(resolver, name, qtype, timeout=timeout, recursion=True)
        except OSError:
            continue
        out += [_address(t, d) for t, d, _p in result['answers'] if t == qtype]
    return out


def resolver_status(resolver, zone, timeout=4.0):
    """How a validating resolver answers the zone's SOA: 'ok', 'servfail', 'nxdomain' or 'error'.

    None when it does not answer. SERVFAIL most often means a DS at the parent that
    matches no key in the zone, or name servers that do not answer for it.
    """
    try:
        result = query(resolver, zone, QTYPE_SOA, timeout=timeout, recursion=True)
    except OSError:
        return None
    if result['rcode'] == RCODE_SERVFAIL:
        return 'servfail'
    if result['rcode'] == RCODE_NXDOMAIN:
        return 'nxdomain'
    if result['rcode'] == RCODE_NOERROR and any(t == QTYPE_SOA for t, _d, _p in result['answers']):
        return 'ok'
    return 'error'


def ds_at_parent(resolver, zone, timeout=4.0):
    """The DS records the parent publishes, as 'tag algorithm type DIGEST'. None: no answer."""
    try:
        result = query(resolver, zone, QTYPE_DS, timeout=timeout, recursion=True)
    except OSError:
        return None
    if result['rcode'] not in (RCODE_NOERROR, RCODE_NXDOMAIN):
        return None
    out = []
    for rtype, rdata, _pos in result['answers']:
        if rtype == QTYPE_DS and len(rdata) > 4:
            tag, algorithm, digest_type = struct.unpack('!HBB', rdata[:4])
            out.append('%d %d %d %s' % (tag, algorithm, digest_type, rdata[4:].hex().upper()))
    return sorted(out)


def is_public(address):
    try:
        return ipaddress.ip_address(address).is_global
    except ValueError:
        return False


def parent_servers(resolver, zone, timeout=3.0):
    """The closest enclosing zone that has name servers, and their names. (None, []) if none found."""
    labels = canonical(zone).rstrip('.').split('.')
    for i in range(1, len(labels)):
        parent = '.'.join(labels[i:]) + '.'
        try:
            result = query(resolver, parent, QTYPE_NS, timeout=timeout, recursion=True)
        except OSError:
            return None, []
        names = [read_name(result['raw'], p) for _o, t, _d, p in result['answer_records']
                 if t == QTYPE_NS and _o == parent]
        if names:
            return parent, sorted(names)
    return None, []


def delegation(resolver, zone, timeout=3.0):
    """What the parent zone itself publishes for zone: the NS names and any glue.

    Asks the parent's own servers, not a resolver, because a resolver answers from
    the child and would hide a registrar entry that differs. Returns None when no
    parent server answered, else {'parent', 'server', 'name_servers', 'glue', 'nxdomain'}:
    name_servers is empty when the parent does not delegate the zone.
    """
    zone = canonical(zone)
    parent, servers = parent_servers(resolver, zone, timeout)
    if not parent:
        return None
    for server in servers:
        for address in resolve_addresses(resolver, server, timeout)[:2]:
            try:
                result = query(address, zone, QTYPE_NS, timeout=timeout)
            except OSError:
                continue
            raw = result['raw']
            # A referral carries the NS in the authority section; a parent that also
            # serves the child answers them directly.
            records = [r for r in result['authority'] + result['answer_records'] if r[1] == QTYPE_NS and r[0] == zone]
            names = sorted({read_name(raw, p) for _o, _t, _d, p in records})
            glue = {}
            for owner, rtype, rdata, _p in result['additional']:
                if rtype in (QTYPE_A, QTYPE_AAAA) and owner in names:
                    glue.setdefault(owner, []).append(_address(rtype, rdata))
            return {'parent': parent, 'server': server, 'name_servers': names,
                    'glue': glue, 'nxdomain': result['rcode'] == RCODE_NXDOMAIN}
    return None
