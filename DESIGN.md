# ns8-powerdns — Design

An authoritative DNS server for NethServer 8, built on PowerDNS Authoritative. It hosts zones,
signs them with DNSSEC, and replicates them to secondary instances on other nodes of the cluster.
It is designed to be driven by [ns8-dnshelper](https://github.com/danb35/ns8-dnshelper), which
adopts its zones automatically, and it also works on its own.

Implement with the `nethserver-ns8-module` skill (NethServer/agents). Items marked **VERIFY**
must be checked against the NS8 developer manual, the PowerDNS documentation or a live node
before code depends on them; do not assume them.

**Starting point.** Generate the repository from
[NethServer/ns8-kickstart](https://github.com/NethServer/ns8-kickstart), not
ns8-kickstart-mariadb. This module needs no MariaDB, no web app and no Traefik route, and the
upstream template carries the current conventions (`%E` in units, `agent.safe_open()`, pinned
Node). Then:

- add `restore-module/`, `bin/module-dump-state` and `etc/state-include.conf` per §10 and the
  skill's `backup-restore.md`;
- apply the GitHub Actions fixes listed in ns8-automx's `CLAUDE.md` (rename the `kickstart`
  placeholders, `permissions: contents: write` on the apidoc workflows, dnshelper's
  `clean-registry.yml`), and add dnshelper's `notify-repomd.yml`.

> Module name: `powerdns` (repository `danb35/ns8-powerdns`, instances `powerdns1`, ...). It
> follows the NS8 habit of naming a module after the software it packages (`mail`, `samba`,
> `nextcloud`). dnshelper also has a provider called `powerdns`, for any PowerDNS server. The two
> are told apart by context: a provider name in a credential, a module id (`powerdns1`)
> everywhere else.

## 1. Goals and non-goals

**Goals (v1)**

- Authoritative-only DNS service for zones the administrator creates.
- DNSSEC signing, per zone, with the DS record shown for the registrar.
- Exactly one primary per cluster and any number of secondaries, at most one instance per node,
  with zones and records replicated automatically.
- Zero-copy-paste integration with dnshelper. When dnshelper is installed, it adopts every zone
  this module serves on its primary, with no credential entered by hand.
- Standalone use. Without dnshelper, a basic Records page lets the administrator edit records.

**Non-goals (v1)**

- Recursion or forwarding. The server never answers for names it is not authoritative for, so
  it cannot be an open resolver. LAN resolution stays with dnsmasq or the Samba DC.
- External peers, meaning secondaries outside the cluster or primaries outside it. The data
  model reserves room for them (§6.5) so that adding them later is additive.
- A full DNS manager. Record editing beyond the basics belongs in dnshelper.
- DNSSEC key rollover automation (§7.4).

**Division of labour with dnshelper**

| ns8-powerdns owns | ns8-dnshelper owns |
|---|---|
| The server: listen addresses, NS name, SOA defaults, replication | Record contents (A, MX, TXT, ...) once it has adopted the zone |
| Zone lifecycle: create, delete, DNSSEC on/off | Which modules may change which records (its policy table) |
| Apex NS and SOA records (dnshelper never changes these) | The full records UI |
| A read-only view of records, editable only in standalone mode | |

## 2. Backend choice: PowerDNS Authoritative

- **API.** dnshelper already has a tested PowerDNS provider (4.9 and 5.0) that lists zones and
  applies each change as one atomic request. With BIND or Knot it would have to use RFC 2136,
  which cannot list zones.
- **Catalog zones (RFC 9432).** PowerDNS 4.7+ can be a catalog producer and consumer. The
  primary adds every zone to its catalog, and secondaries subscribed to the catalog create and
  delete member zones on their own.
- **DNSSEC.** Online signing is enabled by one API field (`dnssec: true`). Outgoing zone
  transfers carry the signatures, so secondaries serve the signed zone without holding keys.

**Image.** `docker.io/powerdns/pdns-auth-50:5.0.8`, the current 5.0 release and the series
dnshelper was tested against. `pdns-auth-51:5.1.5` also exists; move to it after dnshelper's
PowerDNS tests pass against 5.1. Pin the full tag in `org.nethserver.images` so Renovate can
track it.

**Storage.** The gsqlite3 backend: one database file in the module's state, no database
container, and catalog zones are supported. PowerDNS also lists LMDB as catalog-capable, but
gsqlite3 is simpler to dump and inspect, so v1 uses it.

## 3. Instance roles

Each instance is configured as exactly one of:

- **primary**: holds the zones in gsqlite3, signs them, is the catalog producer, serves the API
  to dnshelper and sends NOTIFY to the secondaries.
- **secondary**: subscribes to one primary's catalog, transfers every member zone and serves
  them. It holds no DNSSEC keys and exposes no record-editing API.

`org.nethserver.max-per-node=1`: two instances on one node would fight over port 53.

The role is chosen in `configure-module`. Switching an existing instance between primary and
secondary is not supported in v1: remove it and install it again.

**One primary per cluster.** `configure-module` refuses `role: primary` with the error
`primary_exists` when another module already registers the `powerdns-api` service key (§8.1).
The error names that module, and the instance's own key does not count. The UI then offers only
"secondary", with that primary preselected.

- A secondary still names its primary by module UUID. This keeps the data model ready for
  external primaries later (§6.5); it does not mean several cluster primaries.
- **VERIFY:** that service keys are visible cluster-wide (with `use_replica=True`) at the moment
  `configure-module` runs on a newly added node.
- Two installs racing to become primary at the same moment are not guarded against in v1. The
  second one shows a warning on its Status page once it sees the other key, and §10 covers the
  clone and restore cases.

## 4. Networking

### 4.1 Addresses

- **Public listen addresses.** A list of node IP addresses chosen in the UI, from the node's
  addresses. Never a wildcard by default: the Samba DC, dnsmasq, Pi-hole and AdGuard Home may
  already hold port 53 on some address. `get-configuration` reports, per address, whether 53/udp
  and 53/tcp are free (the Pi-hole module's bind test is a working example).
- **Cluster VPN address.** Always added to the listen list. Zone transfers, NOTIFY and the API
  all travel over the cluster's WireGuard network, so replication and the API are never
  exposed on a public interface.

### 4.2 Container networking

Use `--network=host` for the pdns container, with `local-address` listing the chosen addresses
and the VPN address.

- Host networking keeps clients' real source addresses. PowerDNS checks the source of NOTIFY
  against a zone's primaries, so a rewritten address (as rootless port forwarding may produce)
  would make secondaries ignore NOTIFY.
- It lets PowerDNS bind exactly the addresses chosen, including addresses that appear later.
- **VERIFY:** that a rootless container with host networking can bind port 53 on an NS8 node.
  Pi-hole publishes 53 rootless, which suggests `net.ipv4.ip_unprivileged_port_start` allows
  it. Read the manual pages `rootless_rootfull`, `network` and `port_allocation`.
- **Fallback if host networking is not workable:** keep port publishing, and
  - authenticate everything with TSIG (already the plan, §6.3);
  - set `allow-notify-from` to the address PowerDNS sees for forwarded traffic, or rely on SOA
    refresh polling with a short refresh interval for the catalog zone.

### 4.3 Firewall

- `agent.add_public_service()` opens 53/tcp and 53/udp (authorization `node:fwadm`).
- The API port is never opened publicly.
- **VERIFY:** that the node firewall accepts traffic on the WireGuard interface to the API port
  and to port 53 on the VPN address, without an extra rule.

### 4.4 API endpoint

The PowerDNS webserver/API listens on the VPN address and 127.0.0.1, on a port obtained from
`org.nethserver.tcp-ports-demand=1`.

- `webserver-allow-from` is limited to 127.0.0.1 and the cluster VPN network.
- The traffic is plain HTTP inside WireGuard. The API key travels inside the encrypted tunnel,
  never over a public network. This matches dnshelper's own advice for the PowerDNS provider
  ("a private network").

## 5. Zones

### 5.1 Creating a zone (primary)

`add-zone` input: the zone name, optional DNSSEC settings (§7) and optional SOA overrides. The
module creates it through the API:

- `kind: Primary`, `soa_edit_api: DEFAULT`, `api_rectify: true`. dnshelper requires
  SOA-EDIT-API so that every change raises the serial.
- `catalog`: the instance's producer catalog (§6.1).
- SOA: the primary NS name, the hostmaster address from the configuration, and module-wide
  timers (refresh, retry, expire, minimum).
- Apex NS RRset (§5.2).

Reverse zones (`*.in-addr.arpa`, `*.ip6.arpa`) are created the same way; `add-zone` validates
the name only as a DNS name.

### 5.2 Apex NS records

Each instance has an `ns_name`, the public host name it answers as (`ns1.example.com`), and
an `advertise` flag, on by default.

- The apex NS RRset of every zone is the `ns_name` of every advertised instance: the primary
  plus registered secondaries.
- When a secondary registers or unregisters, the primary rewrites the NS RRset of every zone.
  The change is one API call per zone.
- `add-zone` warns when an `ns_name` lies inside the zone being created, because the registrar
  will then need glue records. It also shows the addresses to use for them.

The module only reports glue; it never sets it, since glue lives at the registrar.

### 5.3 Removing a zone

`remove-zone` deletes the zone, including its keys. The catalog membership disappears with it,
so secondaries drop the zone at the next catalog transfer. The confirmation dialog warns when
DNSSEC is on: a DS record left at the registrar will make the domain fail validation.

## 6. Replication (primary → secondaries)

### 6.1 Catalog

- The primary creates a producer catalog zone `catalog.<module_uuid>.invalid` at configure
  time.
- Every zone the module creates is a member (`catalog` property).
- The catalog is never served publicly, and its name under `.invalid` cannot collide with a
  real zone.
- **VERIFY:** that PowerDNS refuses queries for the catalog from outside the VPN, or restrict
  it with `allow-axfr-ips` and TSIG, so it can only be transferred over the VPN.

### 6.2 Registering a secondary

A secondary instance knows its primary by module UUID, chosen in `configure-module` from the
primary found through service discovery (there is only one, §3).

1. In `configure-module` the secondary calls the primary's `register-secondary` action (role
   `replica`, §9.2) with its `module_id`, VPN address, `ns_name` and `advertise` flag.
2. The primary generates a TSIG key for that secondary (`powerdns-<secondary module id>`,
   hmac-sha256) and stores it with the API (`tsigkeys`). It allows AXFR of the catalog and of
   every member zone for that key, and adds the secondary's VPN address to `also-notify`. It
   updates the apex NS RRsets (§5.2) and returns the key, the primary's VPN address, port and
   the catalog name.
3. The secondary stores the key in its secrets file, creates the consumer zone (`kind:
   Consumer`, primary = the primary's VPN address, transfer key = the key) and retrieves the
   catalog.

`unregister-secondary` reverses this. Removing a secondary module calls it from
`destroy-module`, best effort. If the primary is unreachable, the stale entry is shown on the
primary's Replication page with a Remove button.

**VERIFY:** whether member zones created by a consumer inherit the consumer zone's transfer
TSIG key (metadata `AXFR-MASTER-TSIG`).

- If they do, nothing else is needed.
- If not, the secondary must set the key on each new member. Do this in a small reconcile step
  run by a systemd timer (every minute) and after each catalog transfer: list secondary zones
  and set the missing metadata.

### 6.3 Security

- Every zone transfer and NOTIFY is TSIG-signed with the per-secondary key. TSIG is
  authoritative; addresses are a second check only (`allow-axfr-ips` = cluster VPN network), so
  the design does not depend on source addresses.
- Each secondary has its own key, so removing one secondary revokes exactly that key.

### 6.4 Change propagation

| Change | How secondaries learn of it |
|---|---|
| Records change through dnshelper or the Records page | `SOA-EDIT-API` raises the serial, and the primary sends NOTIFY to `also-notify` |
| New zone | The catalog's serial changes, NOTIFY goes out, the secondary transfers the catalog and creates the member |
| Removed zone | Same path, and the secondary deletes the member |

SOA refresh is the safety net if a NOTIFY is lost.

### 6.5 Room for external peers (not in v1)

Store replication peers on the primary as a list in `state/peers.json`, not as an implied set
of cluster modules:

```json
{"peers": [
  {"id": "powerdns2", "kind": "internal", "address": "10.5.4.2", "tsig_key": "powerdns-powerdns2",
   "ns_name": "ns2.example.com", "advertise": true, "catalog": true}
]}
```

- A later `kind: "external"` peer is the same record, entered by hand: a public address, a key
  pasted in or generated, and `catalog` false for providers that do not consume catalogs. For
  those, the primary would add the peer per zone (`ALSO-NOTIFY` and `TSIG-ALLOW-AXFR` metadata).
- A secondary of an external primary would be a zone with `kind: Secondary` and its own
  `masters` and key. The zone record keeps a `source` field (`local` in v1) for this.
- v1 code only writes `kind: "internal"` peers. Readers must ignore unknown kinds rather than
  fail.

## 7. DNSSEC

### 7.1 Enabling

DNSSEC is a per-zone switch, off by default and offered in `add-zone` and in `update-zone`.
Enabling sets `dnssec: true`, which has PowerDNS create the keys and rectify the zone.

- **Algorithm:** ECDSAP256SHA256 (13), as a single combined key (CSK). Set `default-ksk-algorithm=ecdsa256`
  and `default-zsk-algorithm=` empty in `pdns.conf`. **VERIFY** the setting names for 5.0.
- **Denial of existence:** NSEC3 with RFC 9276 parameters, `1 0 0 -` (no opt-out, 0 extra
  iterations, no salt), as the default; plain NSEC as an option.
- **Narrow NSEC3 is not offered:** it refuses AXFR, which would break secondaries.

### 7.2 What the UI shows

- The zone's DS records (SHA-256), from the cryptokeys API, with a copy button and a note that
  they go to the registrar. **VERIFY** that the cryptokeys endpoint returns `ds`.
- A validation status per zone: "DS published at parent" or "not found". This is a DS query
  for the zone through a public resolver, run on demand from the Zones page, not on a timer.
  It is informational only.

### 7.3 Secondaries

Secondaries receive the signed zone by AXFR and serve it as presigned. **VERIFY:** that a
PowerDNS secondary detects signed transfers and sets PRESIGNED itself; if not, the reconcile
step of §6.2 sets the metadata.

### 7.4 Keys and rollover

- Keys live in the primary's gsqlite3 database, so they are part of its backup (§10). A
  restored primary keeps the same keys and the DS at the registrar stays valid.
- There is no automatic rollover in v1. A CSK with algorithm 13 is commonly kept for years.
  Disabling DNSSEC on a zone deletes its keys; the UI warns the administrator to remove the DS
  at the registrar first and to wait for its TTL.
- A later version may add a manual "roll key" action. Keep key handling in one helper so that
  it can be added without touching zone creation.

## 8. Integration with dnshelper (pull model)

dnshelper discovers the primary and configures itself. The administrator never sees the API
key.

### 8.1 What ns8-powerdns provides

- **Service key** `module/<id>/srv/tcp/powerdns-api` with `host` (VPN address), `port` and
  `role`. Only the primary registers it, and not while in standby (§10).
- **Role `dnsprovider`**, granted from `create-module` grants: `get-provider-config` and
  `list-zones`.
- **`get-provider-config` output:**

  ```json
  {"provider": "powerdns",
   "fields": {"api_url": "http://10.5.4.1:20004", "api_key": "...", "server_id": "localhost"},
   "zones": ["example.com", "example.org"]}
  ```

- **Events** on `module/<id>/event/`:
  - `powerdns-zones-changed` after `add-zone` and `remove-zone`;
  - `powerdns-provider-changed` after anything that changes `fields` (address, port, key
    rotation).

  Payload: `{"module_id", "module_uuid"}`, like other NS8 `*-changed` events.

The API key is generated at install (`create-module/10genpasswords`, `state/passwords.env`,
0600), as the skill's secrets pattern requires. It is never written with `agent.set_env()`.

**VERIFY:** that returning a secret in a task's output is acceptable in NS8. Task output passes
through Redis. If it is not acceptable, dnshelper needs another way to fetch the key, and that
decision must be made before either side is coded.

### 8.2 What ns8-dnshelper must add

These are changes to dnshelper, tracked there.

1. **Authorization label:** `powerdns@any:dnsprovider`. NS8 re-applies grants after every
   `add-module`, so install order does not matter.
2. **Event handlers** `powerdns-zones-changed` and `powerdns-provider-changed`, both running one
   `sync-powerdns` step.
3. **The same sync** from `create-module` (dnshelper installed after the primary) and from a
   **Sync** button on dnshelper's Zones page.
4. **`sync-powerdns` reconcile:**
   1. find the primary through the `powerdns-api` service key; there is at most one (§3);
   2. call its `get-provider-config`;
   3. create or update a credential named after the module (`powerdns1`) and marked
      `managed_by: module/powerdns1`;
   4. add every zone listed that dnshelper does not manage;
   5. remove adopted zones the primary no longer lists;
   6. if the primary is gone, remove its credential and adopted zones.
5. **Managed credential and zones** are read-only in dnshelper's UI. They have no edit or delete
   buttons, but carry an "Adopted from powerdns1" label.
6. **The policy table is not touched.** Adopted zones are default-deny for other modules like
   any other zone, and the administrator adds rules as usual.
7. **Reverse zones:** add `PTR` to the record types of the PowerDNS provider (currently A, AAAA,
   CAA, CNAME, HTTPS, MX, NS, SRV, SVCB, TXT). Without it, PTR records in adopted reverse zones
   could be edited nowhere, since the powerdns Records page is read-only once dnshelper is in
   charge.
8. **Deep link:** support opening the Records page on a given zone (e.g. `?zone=example.com`),
   used by powerdns's read-only view (§9.4). **VERIFY** the NS8 URL form for linking into another
   module's UI.

### 8.3 Who writes records

- While dnshelper manages a zone, the powerdns record actions (`set-records`, `delete-records`)
  refuse with `managed_by_dnshelper`.
- "Managed" is decided by asking dnshelper `has-zone` (role `dnsreader`). If dnshelper does not
  answer, writes are allowed again: a removed dnshelper must not leave zones uneditable.
- Apex NS and SOA are written only by powerdns, which matches dnshelper's rule never to change
  them.

### 8.4 More than one primary key

This should not happen, because of §3 and §10. If dnshelper ever finds more than one
`powerdns-api` key, it adopts nothing new, leaves existing adopted zones alone and logs an error
naming the modules.

## 9. Module interface

### 9.1 Admin actions

| Action | Primary | Secondary | Notes |
|---|---|---|---|
| `configure-module` | ✓ | ✓ | `role`, `ns_name`, `advertise`, `listen_addresses`, `hostmaster`, SOA timers, `primary` (secondary only). `role: primary` is refused with `primary_exists` when another primary exists (§3) |
| `get-configuration` | ✓ | ✓ | Also reports node addresses and port-53 availability, the primary (if any), and whether dnshelper is installed |
| `list-zones` | ✓ | ✓ | Name, DNSSEC state, serial; on a secondary, transfer state and last transfer |
| `add-zone`, `update-zone`, `remove-zone` | ✓ | | `update-zone` changes DNSSEC settings and SOA overrides |
| `get-zone` | ✓ | ✓ | Includes DS records |
| `get-records` | ✓ | ✓ | Read-only on secondaries |
| `set-records`, `delete-records` | ✓ | | Refused while dnshelper manages the zone (§8.3) |
| `list-secondaries`, `remove-secondary` | ✓ | | `remove-secondary` is for stale entries |
| `get-status` | ✓ | ✓ | Service state, per-zone serials, replication lag (secondary serial vs. primary's) |

Records in the powerdns actions use dnshelper's shape (`name` relative to the zone, `type`,
`ttl`, `data` in libdns text form), so the UI code and tests can be shared.

### 9.2 Roles (from `create-module` grants)

| Role | Actions | Granted to |
|---|---|---|
| `replica` | `register-secondary`, `unregister-secondary` | `powerdns@any:replica`, i.e. other powerdns instances |
| `dnsprovider` | `get-provider-config`, `list-zones` | `powerdns@any:dnsprovider`, i.e. dnshelper |

### 9.3 Authorizations declared in `build-images.sh`

```
org.nethserver.authorizations=node:fwadm powerdns@any:replica dnshelper@cluster:dnsreader
```

`dnshelper@cluster:dnsreader` is used only for `has-zone` (§8.3). **VERIFY** that a module can
declare a role on another instance of its own module (`powerdns@any:replica`).

### 9.4 UI pages

- **Settings:**
  - the role, fixed after the first configure;
  - `ns_name` and `advertise`;
  - listen addresses (checkboxes with port-53 availability);
  - hostmaster and SOA timers;
  - on a secondary, the primary to follow.
- **Zones:**
  - primary: list, add, remove, DNSSEC switch, DS records;
  - secondary: read-only list with transfer status.
- **Records:**
  - per zone, read-only by default;
  - editable on a primary only when dnshelper is not installed, or does not manage the zone;
  - when dnshelper manages the zone, a banner: "Records are managed by dnshelper", with a
    button that opens dnshelper's Records page on this zone.
- **Replication (primary):** secondaries with address, NS name, last NOTIFY and serial, and a
  Remove button for stale entries.
- **Status:** service state, per-zone serial and, on a primary, each secondary's lag.

Follow the skill's frontend rules (`Ns*` components first, `isProgressNotified` for long actions).

## 10. Backup and restore

- **Primary:**
  - `module-dump-state` writes a consistent copy of the gsqlite3 database with SQLite's online
    backup, to `state/pdns.sqlite3.backup`;
  - `state-include.conf` lists that file, `state/passwords.env`, `state/peers.json` and the
    config files;
  - the live database file is excluded.
  - Restore puts the copy back before PowerDNS starts. DNSSEC keys are in the database, so DS
    records stay valid.
- **Secondary:** back up configuration and secrets only. Zone data is transferred again from
  the primary after a restore.
- **Clone, move, or restore of a primary while the original still exists:**
  - The copy has the same zones, keys and API key, which would make two primaries.
  - NS8 implements a move as a clone followed by removing the source, so refusing clones would
    also break moves.
  - Instead, a primary copy starts in a **standby** state: PowerDNS runs, but the instance does
    not register the `powerdns-api` key, accept `register-secondary`, or publish events.
  - A reconcile step (the §6.2 timer, and `get-status`) leaves standby once no other primary
    key exists. It then registers the key and publishes `powerdns-replication-changed` and
    `powerdns-provider-changed`, so secondaries re-register and dnshelper updates the API URL.
  - While both exist, the copy's Status page explains the standby and names the other primary.
  - **VERIFY:** the order of steps in an NS8 move (clone, then source removal), and whether
    `clone-module` can tell a move from a plain clone; if it can, standby is only needed for
    plain clones.
- **Restore under a new module id:**
  - TSIG key names embed secondary ids, so after restoring a primary, every secondary must
    re-register;
  - `restore-module` on the primary publishes `powerdns-replication-changed`;
  - secondaries handle that event by calling `register-secondary` again.

Follow the skill's `backup-restore.md`; in particular, `50call-configure-module` must pass every
variable restored by `06copyenv`.

## 11. Testing

- **Robot tests:** install, configure as primary, add a zone, query it with `dig`, enable
  DNSSEC and validate with `delv` (or check RRSIG presence), remove, uninstall.
- **Two-node test** (may be manual at first):
  - install a secondary;
  - check that the catalog is transferred, member zones appear, a record change reaches the
    secondary within seconds (NOTIFY), and a zone removal propagates;
  - check that `unregister-secondary` revokes the key, so that AXFR with the old key is refused.
- **dnshelper integration test:**
  - install both;
  - check that dnshelper adopts the zones with no input;
  - check that a record written through dnshelper's `append-records` is served by powerdns and
    by the secondary;
  - check that powerdns's `set-records` returns `managed_by_dnshelper`.
- **One-primary test:**
  - with a primary installed, `configure-module` with `role: primary` on a second node
    returns `primary_exists`;
  - a clone of the primary starts in standby, and leaves it when the source is removed.
- **Port conflict test:** with Samba DC or dnsmasq on the same node, `get-configuration` reports
  the conflicting address as busy and `configure-module` refuses it.

## 12. Open items

1. The **VERIFY** items above. The ones that can change the design are:
   - host networking (§4.2);
   - secrets in task output (§8.1);
   - TSIG inheritance for catalog members (§6.2);
   - how NS8 sequences a move (§10).
2. A manual DNSSEC key-roll action, for a later version.

## 13. Community requests (for the release announcement)

Forum threads asking for an authoritative DNS server in NethServer, newest first. Link these in
the release announcement.

| Thread | Posts that ask for it | Version |
|---|---|---|
| [Ns8-dnshelper - Tool to allow other modules to control your DNS records](https://community.nethserver.org/t/ns8-dnshelper-tool-to-allow-other-modules-to-control-your-dns-records/28774) (Sep 2026) | [#11](https://community.nethserver.org/t/ns8-dnshelper-tool-to-allow-other-modules-to-control-your-dns-records/28774/11): Giacomo Sanchietti would like authoritative DNS servers inside NethServer that apps update automatically. [#12](https://community.nethserver.org/t/ns8-dnshelper-tool-to-allow-other-modules-to-control-your-dns-records/28774/12): Dan suggests a DNS server package that dnshelper could drive. | NS8 |
| [API-based DNS management](https://community.nethserver.org/t/api-based-dns-management/26845) (Jan 2026, Dan) | #1 refers back to the earlier proposal of NS8 as its own authoritative DNS host | NS8 |
| [DNS module](https://community.nethserver.org/t/dns-module/22995) (Feb 2024, MrGenius) | #1 asks whether NS8 will add a full authoritative DNS server alongside dnsmasq; [#16](https://community.nethserver.org/t/dns-module/22995/16) and [#20](https://community.nethserver.org/t/dns-module/22995/20) by Dan make the case, including a second, geographically separate server | NS8 |
| [Full, public, authoritative DNS support](https://community.nethserver.org/t/full-public-authoritative-dns-support/18692) (Jul 2021, Dan) | #1 is the request, with email's DNS records as the motivation. [#6](https://community.nethserver.org/t/full-public-authoritative-dns-support/18692/6): Giacomo says the team hoped to have an authoritative DNS server inside NS8. Later replies suggest PowerDNS and BIND | NS7, looking ahead to NS8 |
| [Full DNS software, even via docker](https://community.nethserver.org/t/full-dns-software-even-via-docker/16787) (Oct 2020, MrGenius) | #1 asks for a full DNS server that can host A, AAAA, MX and TXT records, ideally built in | NS7 |
| [NethServer as public DNS authoritative server](https://community.nethserver.org/t/nethserver-as-public-dns-authoritative-server/15240) (Apr 2020, Marco Marinello) | #1 asks to use NethServer as a domain's public authoritative server | NS7 |
| [NethServer 8: wishlist for the conference](https://community.nethserver.org/t/nethserver-8-wishlist-for-the-conference/6608) (2019) | [#76](https://community.nethserver.org/t/nethserver-8-wishlist-for-the-conference/6608/76) (Nick Sardelianos) and [#81](https://community.nethserver.org/t/nethserver-8-wishlist-for-the-conference/6608/81) (Gabriel Gheorghiu) ask for a full, authoritative DNS server in NS8 | NS8 wishlist |

Not included because they are about LAN DNS or replacing dnsmasq, not authoritative hosting:
[NethServer 8 built in DNS](https://community.nethserver.org/t/nethserver-8-built-in-dns/21400) and
[How about PowerDNS?](https://community.nethserver.org/t/how-about-powerdns/3131).