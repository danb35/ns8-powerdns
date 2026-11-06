# VERIFY results

DESIGN.md marks items to check before code depends on them. These are the results, and how each was
checked. "Live" means PowerDNS 5.0.8 in Docker (`tests/unit/test_live_pdns.py` keeps the checks that
can be automated). "Source" means ns8-core or PowerDNS source (`rel/auth-5.0.x`).

**LAN node, 2026-11-05 (one node, Rocky 9.8, core 3.24):** a primary was installed from a build on the
node, through a temporary local registry, and updated once. Checked there: rootless host networking on
port 53 with no SELinux denials, the firewall service, the service key, every primary action, a real
`has-zone` answered by dnshelper, the backup dump and cleanup scripts, the reconcile timer, and the UI
pages in a browser. A DNS client on the LAN got signed answers and NSEC3 denial, and was refused
recursion and unsigned AXFR; the API did not answer from the LAN.

**QEMU, 2026-11-05 (Rocky 9 and Debian 13):** the Robot suite passes on both, including install,
configuration, zones, records, DNSSEC, the backup scripts and removal. On Rocky 9 it also takes
screenshots of every page.

**Two nodes, 2026-11-05 (Rocky 9.8 and Debian 13, one cluster):** a primary on one and a secondary on the
other, in both directions. `primary_exists` refuses; the secondary transfers its zones and serves them
signed without keys; a record change arrived in 6 to 11 seconds, a new zone in about a minute, a removal in
8 seconds. A client on the LAN got signed answers from the secondary, was refused recursion and AXFR, and
could not reach its API. Removing a secondary rewrites the NS records and revokes its key.

**Backup, restore and copies, same day:** with NS8's `cluster` backup target, on the node itself. Each of
these kept the zones, DS record and API key: restore next to the original, restore with `replace`, restore
after losing the original, restore to another node, plain clone, and move. A restored primary keeps its
secondary following; a restored secondary serves again about a minute after its restore finishes. A copy
on another node runs in standby and refuses writes, and takes over within seconds of the original going.

**dnshelper integration, same day:** a primary on Debian and a secondary on Rocky, with `dnshelper3`
built from danb35/ns8-dnshelper master `9c62af0` and `dnshelper1` (0.4.6) as the cluster default. A new
zone was adopted within 5 seconds, with a credential marked `managed_by` and the API key never shown.
Records written with dnshelper's `append-records` were served by the primary at once and by the secondary
within 20 seconds. dnshelper refused changes to the adopted zone and credential. Removing the zone in
powerdns, and later removing the primary, each made dnshelper drop what it had adopted within 5 seconds.
`set-records` and `delete-records` were refused with `managed_by_dnshelper` only after the fix below.

**UI and edge cases, same day:** with a primary on Debian, a secondary on Rocky and `dnshelper3`
adopting. The Records page of an adopted zone shows the dnshelper banner and no edit buttons, and its
link opens `dnshelper3`'s Records page on that zone. Every page was rendered in all nine translations
with no missing key, raw key name or overflowing text; Arabic and Tamil were also checked by eye. A
secondary listening on its IPv6 address answered over UDP and TCP from the LAN, and refused recursion
and AXFR there. On 2026-11-06 a primary on a single-node VPS (Rocky 9.8, core 3.24), listening on its
public IPv6 address, was queried from another host on the internet: a signed record came back over
UDP with its RRSIG and over TCP, both authoritative; the DNSKEY was signed; a name outside its zones
was `REFUSED`; and AXFR failed. The same day, the released dnshelper 0.5.0 adopted a zone from a new
primary within 14 seconds, its records were served, powerdns refused direct edits, and dnshelper
dropped the zone 3 seconds after it was removed. The delegation check's comparison was run against
real zones from the Mac: `2v6.in` matched its Cloudflare delegation as read from the `.in` registry's
own servers; with a made-up name server it listed that name as missing and Cloudflare's as not
served here; `bbc.co.uk` returned its glue from `.co.uk`; an undelegated name read as not
delegated; and `dnssec-failed.org` gave a stale DS and SERVFAIL. Then against a real delegation: `demo.2v6.in`,
delegated from Cloudflare to a primary on the VPS. With a second NS name the VPS did not serve
and no DS, the check reported that name as not served here and the DS as missing, with glue and
resolution OK. Once the extra name was removed and the DS added, every line was OK, including
validation through 1.1.1.1. With the dnsmasq module holding port 53 on node 1, Settings showed those addresses as
in use and `configure-module` refused them with `address_busy`. Removing a secondary and saving its
settings again re-registers it.

**Not tested:** a move with a secondary present, which
needs three nodes; a clone from Rocky to Debian, because of the core issue below.

## Results

| Section | Question | Result | How |
|---|---|---|---|
| 3 | Service keys visible when `configure-module` runs on a new node | Actions read the leader, not a replica, and fall back to the replica only if the leader is down | Source; nodes |
| 4.2 | Rootless host networking can bind 53 | Yes: core sets `ip_unprivileged_port_start=23`, and the manual documents `--network=host` | LAN node |
| 4.3 | Firewall allows the VPN to reach the API and 53 | Yes: the VPN is the `trusted` zone, where any connection is allowed | Manual; two nodes |
| 6.1 | Catalog refused outside the VPN | **No**, see below | Live |
| 6.2 | Members inherit the consumer's TSIG key | **No**: reconcile timer needed | Live |
| 7.1 | Setting names for a combined key | `default-ksk-algorithm=ecdsa256`, `default-zsk-algorithm=` empty; gives one `csk` | Live |
| 7.2 | Cryptokeys endpoint returns `ds` | Yes, SHA-256 and SHA-384; the module shows SHA-256 | Live |
| 7.3 | Secondary sets PRESIGNED itself | Yes, and serves RRSIGs with no keys | Live |
| 8.1 | Secret in task output acceptable | Yes, see below | Source |
| 8.2 | URL for linking into another module | `/apps/<id>?page=<page>`, query parameters allowed. dnshelper must add `zone` | Source |
| 9.3 | A module can hold a role on its own module | Yes: `@any` becomes the pattern `module/powerdns*` | Source; nodes |
| 9.3 | `dnshelper@cluster` reaches every dnshelper | **No**: only the default instance; `@any` is needed | Nodes |
| 10 | Order of a move; can clone tell a move | Clone, then source removal; `replace` is in the clone and restore requests | Source |

## Where testing changed the design

**Catalog serial (6.1).** A producer zone's serial goes to the current epoch time when a member
changes. An API-created zone starts with a date-style serial such as `2026110501`, which is higher, so
consumers logged "more recent than primary" and never saw a new zone. The catalog is created with
serial 1 and no SOA-EDIT-API.

**NOTIFY is not TSIG-signed (6.3).** PowerDNS signs a NOTIFY with the zone's first `TSIG-ALLOW-AXFR`
key, and a secondary refuses any other. With per-secondary keys, the second secondary answered
"Not Authorized" and only caught up at SOA refresh. So `send-signed-notify=no` on the primary, and
`allow-notify-from=<primary VPN address>/32` on each secondary. An unsigned NOTIFY grants nothing: it
only prompts a SOA check, and the transfer itself still needs the key.

**Addresses are not a second check on AXFR (6.3).** A valid TSIG key is accepted whatever the source
address, and an unsigned request from an `allow-axfr-ips` address is accepted with no key. Setting that
list to the VPN network, as the design proposed, would let any cluster node transfer any zone unsigned.
The list is empty, which makes TSIG mandatory. This is stricter than the design.

**Per-zone `ALSO-NOTIFY`, not the global `also-notify` (6.2).** Changing the global setting needs a
restart of the DNS server each time a secondary registers. The metadata applies at once. `only-notify=`
is empty, so PowerDNS does not also notify whatever the NS names resolve to.

**Propagation time (6.4, 11).** The primary looks for changed serials each `xfr-cycle-interval`, default
60 seconds, so "within seconds" needs a shorter one. It is 10 here, which gave 6 to 10 seconds live.

**The catalog can be queried publicly (6.1).** Its SOA and other records answer from any address;
PowerDNS has no per-zone query ACL short of views. AXFR, the only way to list it, needs a key, which is
the design's stated alternative. Exposure: a client who already knows a zone name can derive its member
label, and learns only that the zone is hosted here, which is public anyway.

**The API has one listen address (4.4).** `webserver-address` takes a single address, so a primary's API
is on the VPN address only and local actions call it there. A secondary's is on 127.0.0.1 only, used by
its own actions to manage the consumer zone.

**Secret in task output (8.1).** Precedent: ns8-mail's `reveal-master-credentials` returns a password
the same way. Redis ACLs limit a module to its own `task/module/<id>/*` keys and the default user cannot
read `task/` at all, so the output is not visible to other modules, unlike `state/environment`. It does
pass through Redis, and is visible to cluster administrators, who can read the key anyway.

**A copy on its original's node cannot run (10).** Both need port 53 on the VPN address, and the core
removes the original only after the copy has succeeded. So a restore with `replace` failed on a one-node
cluster. Such a copy now finishes without starting, and the timer starts it when the other instance is gone.

**An instance's role on itself is unreliable (9.3).** `powerdns@any:replica` also matches the instance, and
the core keeps one role per agent, last grant wins, in the order of a Redis set. So `replica` could replace
`selfadm`, and the usual `50call-configure-module` got a 403 in some restores and not others. `restore-module`
runs the steps directly instead. The Robot suite now restores from a real backup.

**Only the default dnshelper was asked (8.3, 9.3).** powerdns found dnshelper with `dnshelper@cluster`, which
is the default instance, and held `dnsreader` only there. With an older default and a newer instance
adopting the zones, the default said "not managed" and powerdns allowed edits to adopted zones. powerdns
now asks every dnshelper instance, holds `dnshelper@any:dnsreader`, and links to the instance that
manages the zone.

**Remove dropped a working secondary (6.2, 9.4).** The Replication page offered Remove on every
secondary, with no confirmation. A secondary removed while running stayed installed and kept serving its
zones at a frozen serial, with nothing on its pages to say so. Remove is now offered only for a secondary
that does not answer, behind a confirmation, and `remove-secondary` refuses a reachable one with
`secondary_reachable`. Reachability now includes the catalog, so a secondary with no zones yet is not
reported unreachable. Retested: refused while running, offered and confirmed once it was stopped.

**The UDP port check missed a listener (4.3).** The probe set `SO_REUSEADDR` on its UDP socket too, which
on Linux lets it bind beside another program's reuse-enabled socket. With dnsmasq on the address, UDP read
as free and only the TCP check caught the conflict. The option is now set only on the TCP probe; retested
with a UDP-only listener, which now reads as busy.

**`pt_BR` was never used (UI).** The template picks the translation from the first two letters of the
browser's language, so a Brazilian browser got `pt`. The UI now tries the regional folder first
(`pt-BR` → `pt_BR`). The code comes from the module template, so other modules built from it likely
have the same limitation.

**The timer drifted (6.2).** systemd's default `AccuracySec` of one minute put runs two minutes apart, which
held up a restored secondary for over three minutes. It is 5 seconds now.

## Other findings

- **Core: a clone from Rocky to Debian fails.** On core 3.24, `clone-module`'s `90finalize` tries to enable
  `grub-boot-success.timer`, a Rocky unit listed by the source, and aborts on Debian. This is not specific to
  this module. Debian to Rocky works. The current ns8-core source filters such units, so a newer core may
  have fixed it.
- **PowerDNS polls for security status at startup** ("Polled security status of version 5.0.8"), a DNS query
  that discloses its version to the PowerDNS project. It only logs a warning, and updates reach
  administrators through module releases, so `security-poll-suffix=` is now empty and the poll is off.
  Checked in a 5.0.8 container: no poll is logged with that setting.
- **PowerDNS 5.1.5 mangles TXT escaping through the API.** Tested before moving to 5.1: content with an
  escaped quote (`"a \"q\" b"`) is refused with 422, and an escaped backslash is stored and served without
  it (`back\slash` becomes `backslash`). 5.0.8 handles both. This broke a powerdns live test added for the
  case, and dnshelper's `TestLiveTXTQuotesAndBackslashes`; everything else passed on 5.1.5. Upstream:
  PowerDNS/pdns#18159, fixed in master by #18176, not yet in a 5.1 release. The module stays on 5.0.8
  (DESIGN 2).

## Decisions beyond the design

- **`get-dns-status`, not `get-status`.** The core owns `get-status`, which the Status page uses for
  services and images. DESIGN 9.1's extra data has its own action.
- **A standby refuses writes.** Zone and record changes are refused with `primary_standby`. The design
  only stops registration and events, but a standby accepting edits would lose them on takeover.
- **`get-zone` on a secondary has no DS records.** It holds no keys. The primary's `get-zone` shows them.
- **Peers carry an extra `addresses` field**, the secondary's public addresses, so `add-zone` can report
  glue for names inside the zone. Readers ignore fields they do not use.
- **Removing a primary** publishes `powerdns-provider-changed`, after deleting its service key, unless
  another module holds its UUID (a move). dnshelper can then drop the credential at once.
