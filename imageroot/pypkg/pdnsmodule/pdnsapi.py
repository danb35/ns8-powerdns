#
# Copyright (C) 2026 Dan Brown
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""A small client for the PowerDNS Authoritative HTTP API."""

import json
import time
import urllib.error
import urllib.parse
import urllib.request


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__('PowerDNS API %s: %s' % (status, message))
        self.status = status
        self.message = message


class Pdns:
    def __init__(self, base_url, api_key, timeout=30):
        self.base = base_url.rstrip('/') + '/api/v1/servers/localhost'
        self.api_key = api_key
        self.timeout = timeout

    def call(self, method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        request = urllib.request.Request(self.base + path, data=data, method=method, headers={
            'X-API-Key': self.api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read()
        except urllib.error.HTTPError as e:
            raw = e.read().decode(errors='replace')
            try:
                message = json.loads(raw).get('error', raw)
            except ValueError:
                message = raw
            raise ApiError(e.code, message) from None
        return json.loads(raw) if raw else None

    def wait_ready(self, seconds=30):
        deadline = time.time() + seconds
        while True:
            try:
                return self.call('GET', '')
            except (OSError, ApiError):
                if time.time() >= deadline:
                    raise
                time.sleep(1)

    @staticmethod
    def _zid(zone):
        return urllib.parse.quote(zone, safe='')

    def zones(self):
        return self.call('GET', '/zones')

    def zone(self, zone, rrsets=True):
        return self.call('GET', '/zones/%s?rrsets=%s' % (self._zid(zone), 'true' if rrsets else 'false'))

    def zone_or_none(self, zone):
        try:
            return self.zone(zone, rrsets=False)
        except ApiError as e:
            if e.status == 404:
                return None
            raise

    def create_zone(self, body):
        return self.call('POST', '/zones', body)

    def update_zone(self, zone, body):
        self.call('PUT', '/zones/%s' % self._zid(zone), body)

    def delete_zone(self, zone):
        self.call('DELETE', '/zones/%s' % self._zid(zone))

    def patch_rrsets(self, zone, rrsets):
        self.call('PATCH', '/zones/%s' % self._zid(zone), {'rrsets': rrsets})

    def cryptokeys(self, zone):
        return self.call('GET', '/zones/%s/cryptokeys' % self._zid(zone))

    def set_metadata(self, zone, kind, values):
        if values:
            self.call('PUT', '/zones/%s/metadata/%s' % (self._zid(zone), kind), {'kind': kind, 'metadata': values})
        else:
            self.call('DELETE', '/zones/%s/metadata/%s' % (self._zid(zone), kind))

    def metadata(self, zone, kind):
        return self.call('GET', '/zones/%s/metadata/%s' % (self._zid(zone), kind)).get('metadata', [])

    def retrieve(self, zone):
        return self.call('PUT', '/zones/%s/axfr-retrieve' % self._zid(zone))

    def tsigkey(self, key_id):
        try:
            return self.call('GET', '/tsigkeys/%s' % urllib.parse.quote(key_id, safe=''))
        except ApiError as e:
            if e.status == 404:
                return None
            raise

    def create_tsigkey(self, name, secret=None):
        body = {'name': name, 'algorithm': 'hmac-sha256'}
        if secret:
            body['key'] = secret
        return self.call('POST', '/tsigkeys', body)

    def delete_tsigkey(self, key_id):
        try:
            self.call('DELETE', '/tsigkeys/%s' % urllib.parse.quote(key_id, safe=''))
        except ApiError as e:
            if e.status != 404:
                raise
