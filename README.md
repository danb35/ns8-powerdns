# ns8-powerdns

An authoritative DNS server for [NethServer 8](https://github.com/NethServer/ns8-core), built on
[PowerDNS Authoritative](https://doc.powerdns.com/authoritative/). It hosts zones, signs them with
DNSSEC, and replicates them to secondary instances on other nodes of the cluster.

It works on its own, with a basic Records page, and is designed to be driven by
[ns8-dnshelper](https://github.com/danb35/ns8-dnshelper) 0.5.0 or later, which adopts its zones
automatically.

**Administering it?** The [user guide](docs/USER-GUIDE.md) explains setting up the primary and its
secondaries, adding zones, and what to enter at your registrar: name servers, glue records and the
DS record, and in which order when moving a live domain.

The server is authoritative only. It never recurses or forwards, so it cannot be an open resolver;
LAN name resolution stays with dnsmasq or the Samba DC.

See [DESIGN.md](DESIGN.md) for the design and [docs/VERIFY.md](docs/VERIFY.md) for what was verified
and how, including where testing changed the design.

## Install

### From the Software center (recommended)

powerdns is published in the software repository at
[danb35.github.io/ns8-repomd](https://danb35.github.io/ns8-repomd/) (source:
[danb35/ns8-repomd](https://github.com/danb35/ns8-repomd)). Add it to the cluster once:

1. In the cluster admin UI, open **Settings → Software repositories** and click **Add repository**.
2. Enter a name (for example `danb35`) and the URL `https://danb35.github.io/ns8-repomd/`, leave
   **Status** enabled, and click **Add repository**. NS8 warns about third-party repositories;
   this one only lists the images published from this GitHub account.
3. Open the **Software center**, find **powerdns**, and click **Install**. It needs NS8 core
   3.18.0 or later. Install it on the node
   that will hold the primary, then again on each node that will hold a secondary.

Or add the repository from a shell on the leader node:

    api-cli run add-repository --data '{"name":"danb35","url":"https://danb35.github.io/ns8-repomd/","status":true}'

With the repository added, new releases are offered as updates in the Software center like any
other app.

To have [dnshelper](https://github.com/danb35/ns8-dnshelper) adopt the zones, install dnshelper
0.5.0 or later from NethForge: on the same page, enable the `nethforge` repository, which every
cluster already has, disabled by default.

### From the command line

    add-module ghcr.io/danb35/powerdns:latest 1

The output names the instance, for example `powerdns1`. At most one instance runs per node, because
two would compete for port 53.

## Configure

Each instance is either the cluster's only **primary** or a **secondary** of it. The role cannot be
changed later: remove the instance and install it again.

`configure-module` takes:

- `role`: `primary` or `secondary`;
- `ns_name`: the public host name this instance answers as, such as `ns1.example.com`;
- `advertise`: whether to list this instance in the apex NS of every zone (default `true`);
- `listen_addresses`: node addresses to serve DNS on. The cluster VPN address is always added;
- `hostmaster`: the SOA contact, required on a primary;
- `soa_refresh`, `soa_retry`, `soa_expire`, `soa_minimum`: module-wide SOA timers, in seconds;
- `primary`: on a secondary, the module UUID of the primary (`get-configuration` lists it).

Install and configure the primary first:

    api-cli run module/powerdns1/get-configuration
    api-cli run module/powerdns1/configure-module --data '{"role":"primary","ns_name":"ns1.example.com","hostmaster":"hostmaster@example.com","listen_addresses":["192.0.2.1"]}'

`get-configuration` reports whether port 53 is free on each address. Samba DC, dnsmasq, Pi-hole and
AdGuard Home may already hold it. Zones are managed from the UI or with `add-zone`, `update-zone` and
`remove-zone`:

    api-cli run module/powerdns1/add-zone --data '{"zone":"example.com","dnssec":true}'
    api-cli run module/powerdns1/get-zone --data '{"zone":"example.com"}'

`get-zone` returns what the registrar needs: the name servers, which of them need glue records and
their addresses, and, for a signed zone, the DS and DNSKEY records. `add-zone` also lists the glue.
Once the registrar has them, `check-delegation` compares what the parent zone publishes with what the
zone needs:

    api-cli run module/powerdns1/check-delegation --data '{"zone":"example.com"}'

The [user guide](docs/USER-GUIDE.md#at-the-registrar) explains each entry.

## Replication

A new secondary registers with the primary and receives its own TSIG key. It learns the zones from a
catalog zone (RFC 9432), so new and removed zones reach it without any action. Transfers need that key:
no address is allowed to transfer a zone without one. All replication travels over the cluster VPN.

A record change reaches the secondaries within about ten seconds. A new zone takes up to a minute
more, because a timer on the secondary gives each new zone its transfer key.

If a secondary was removed while the primary was unreachable, remove its entry from the Replication
page.

## Backup, clone and move

A primary's backup holds a consistent copy of the database, including the DNSSEC keys, so the DS at
the registrar stays valid after a restore. A secondary's backup holds its configuration only, and it
transfers its zones again.

A clone or restore of a primary starts in **standby** while another primary exists: it serves its
zones but takes no changes. It takes over within a minute of the other primary being removed, which is
also how a move works. Secondaries and dnshelper then follow it by themselves.

## Uninstall

    remove-module --no-preserve powerdns1

Removing a primary leaves its secondaries serving the last copy of the zones.

## Development

Python unit and live tests, against real PowerDNS servers in Docker:

```bash
python3 -m unittest discover -s tests/unit -v
```

The end-to-end suite is in `tests/powerdns.robot`, with the NS8 standard
[testing infrastructure](https://github.com/NethServer/ns8-github-actions/blob/v1/README.md#running-tests-locally).
Its `ui`-tagged cases take screenshots of every page. They run when `ui/` or `build-images.sh` changes,
which includes Renovate's pull requests, or on demand with the `ui_tests` input of the "Test module"
workflow. On a pull request the images go to the `ci-screenshots` branch and are linked from a comment;
otherwise they are in the run's artifacts.

Releases: tags are plain semver without a `v`, annotated, on a commit whose checks all passed. To have
[ns8-repomd](https://github.com/danb35/ns8-repomd) rebuild at once, set the `REPOMD_DISPATCH_TOKEN`
secret; without it the release appears at the next scheduled build.

## UI translation

Edit only `ui/public/i18n/en/translation.json`. Other languages are translated with
[Weblate](https://hosted.weblate.org/projects/ns8/).
