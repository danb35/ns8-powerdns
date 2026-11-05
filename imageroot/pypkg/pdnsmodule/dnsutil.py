#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""DNS names, record conversion and a minimal stub query, standard library only.

The NS8 agent environment has no DNS library, and the module needs only a SOA
serial and "does a DS record exist".
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

QTYPE_SOA = 6
QTYPE_DS = 43


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


def query(server, name, qtype, port=53, timeout=3.0, recursion=False):
    """One UDP query. Returns {'rcode': int, 'answers': [(type, rdata bytes)]}.

    Raises OSError when the server does not answer.
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
    qdcount, ancount = struct.unpack('!HH', buf[4:8])
    pos = 12
    for _ in range(qdcount):
        pos = _skip_name(buf, pos) + 4
    answers = []
    for _ in range(ancount):
        pos = _skip_name(buf, pos)
        rtype, _klass, _ttl, rdlength = struct.unpack('!HHIH', buf[pos:pos + 10])
        pos += 10
        answers.append((rtype, buf[pos:pos + rdlength], pos))
        pos += rdlength
    return {'rcode': rcode, 'answers': answers, 'raw': buf}


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


def ds_published(resolver, zone, timeout=4.0):
    """True/False: does the parent publish a DS. None: the resolver did not answer."""
    try:
        result = query(resolver, zone, QTYPE_DS, timeout=timeout, recursion=True)
    except OSError:
        return None
    if result['rcode'] not in (0, 3):
        return None
    return any(rtype == QTYPE_DS for rtype, _rdata, _pos in result['answers'])
