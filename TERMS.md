# Data and privacy

powerdns has no telemetry, and nothing is sent to its author. It runs on your own node. PowerDNS's
own security poll, which would send its version number to the PowerDNS project, is turned off.

## What anyone on the internet can learn

An authoritative DNS server exists to answer questions about your zones, so anyone who can reach
port 53 on the addresses you choose can ask for any record in them. The node's firewall opens
port 53 (UDP and TCP) for this instance.

| Data | Depends on |
|---|---|
| Any record in your zones, by its name | Always: that is the server's job |
| Every name in a zone, by walking it | **Signed zones with NSEC**: the whole zone can be listed. NSEC3, the default, hides names behind hashes, but common names can still be guessed offline |
| The names of your name servers, and their addresses where glue is needed | Always, in each zone's NS records and at your registrar |
| That this is PowerDNS, or which version | Not given: the version answer is "anonymous" |

The server does not resolve other names, and its API answers only on the cluster VPN (on a primary)
or the node itself (on a secondary). It refuses zone transfers to anyone without a key, except from
the addresses you enter for an external secondary set to transfer by address: anyone who can send
from those addresses can read every record of the zones given to it.

## What goes where

| Data | Where it goes | When |
|---|---|---|
| Your zones and records, including signatures for signed zones | The secondaries you install in your cluster, over the cluster VPN, with a key for each secondary | On every change |
| The zones you give an external secondary, every record in them, and the node's public address | That secondary, such as a provider's secondary DNS service, over the internet. TSIG keeps transfers from being altered but does not encrypt them, so anyone on the path can read them | Only if you add an external secondary, on every change to those zones |
| The names of the zones given to an external secondary | Its NOTIFY addresses, asked for each zone's serial | When the Replication page shows the external secondary's state |
| The zone's name, and the node's IP address | Cloudflare (1.1.1.1) and, if it does not answer, Quad9 (9.9.9.9); and the name servers of the zone above yours, such as the `.com` registry's for `example.com` | Only when you choose **Check the parent zone** |
| The API key, and through it full control of the zones | [dnshelper](https://github.com/danb35/ns8-dnshelper), on its request | Only if dnshelper is installed in the cluster. See [dnshelper's own page](https://github.com/danb35/ns8-dnshelper/blob/master/TERMS.md) |
| Zones, records, DNSSEC private keys, the API key, the secondaries' keys and the external secondaries' settings and keys | Your backup destination, encrypted by NS8 | If you have configured backups |
| PowerDNS's log: zone names, transfers, notifications, and the addresses of the servers involved. Queries are not logged | NS8's log server, and any syslog server or Cloud Log Manager you forward logs to | As it happens |

Your registrar receives your name servers, glue records and DS record only when you enter them there
yourself: powerdns does not contact registrars. How Cloudflare, Quad9, the registries and your
registrar handle data is governed by their own terms, and so is how the provider of an external
secondary handles your zones and the queries it answers for them.

## What is kept on the node

These files are in the module's state directory:

- the PowerDNS database: zones, records and, on a primary, the DNSSEC private keys and the
  secondaries' transfer keys, external ones included. It is not encrypted on the node.
- `passwords.env`, mode 0600: the API key and, on a secondary, its transfer key. These are not
  stored in Redis.
- `peers.json`, on a primary: the secondaries, with their VPN addresses and name server names, and
  the external secondaries, with their names, NOTIFY addresses, allowed source addresses, name
  servers and zones.

Cluster administrators can read all of this, and cloning or moving the module copies it, keys
included, to the new instance.

## What it is allowed to do on your cluster

- `node:fwadm`, to open port 53 for this instance. The role also allows other firewall changes;
  powerdns adds and removes only its own service.
- `powerdns@any:replica`, so that secondaries can register with the primary and unregister.
- `dnshelper@any:dnsreader`, used only to ask dnshelper whether it manages a zone. The role also
  allows listing zones and reading records through dnshelper, as far as dnshelper's access rules
  permit; powerdns does not use it for that.

The code is public, so you can check this.

## Removing data

Removing a zone deletes it, its records and, for a signed zone, its DNSSEC keys, here and on every
secondary. If your registrar still publishes a DS record for it, remove that first, or the domain
fails validation. Removing the module deletes its state directory. Older backups and logs keep what
they already hold.

An external secondary is not in your cluster, so nothing here can delete what it holds. Removing a
zone, or the external secondary, or taking a zone off its list, stops further transfers and revokes
its access, but the copy it already has stays there until you delete it at the provider.

## License

powerdns is free software under the [GNU General Public License v3](LICENSE) or later. It runs
the [PowerDNS Authoritative Server](https://github.com/PowerDNS/pdns) container image, which is
licensed under the GNU General Public License v2.
