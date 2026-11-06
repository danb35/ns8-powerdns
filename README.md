# README

## Top-level Schemas

* [add-zone input](./add-zone-input.md "Create a zone on the primary") – `http://schema.nethserver.org/powerdns/add-zone-input.json`

* [add-zone output](./add-zone-output.md "Create a zone on the primary") – `http://schema.nethserver.org/powerdns/add-zone-output.json`

* [check-delegation input](./check-delegation-input.md "Compare what the parent zone publishes for a zone with what the zone needs at the registrar") – `http://schema.nethserver.org/powerdns/check-delegation-input.json`

* [check-delegation output](./check-delegation-output.md "Compare what the parent zone publishes for a zone with what the zone needs at the registrar") – `http://schema.nethserver.org/powerdns/check-delegation-output.json`

* [configure-module input](./configure-module-input.md "Configure the instance as the cluster's primary or as a secondary") – `http://schema.nethserver.org/powerdns/configure-module-input.json`

* [delete-records input](./delete-records-input.md "Delete RRsets or single values") – `http://schema.nethserver.org/powerdns/delete-records-input.json`

* [delete-records output](./delete-records-output.md "Delete RRsets or single values") – `http://schema.nethserver.org/powerdns/delete-records-output.json`

* [get-configuration output](./get-configuration-output.md "Current configuration, node addresses with port 53 availability, the primary if any, and dnshelper") – `http://schema.nethserver.org/powerdns/get-configuration-output.json`

* [get-dns-status output](./get-dns-status-output.md "Per-zone serials, replication lag and standby state, for the Status page") – `http://schema.nethserver.org/powerdns/get-dns-status-output.json`

* [get-provider-config output](./get-provider-config-output.md "Role dnsprovider") – `http://schema.nethserver.org/powerdns/get-provider-config-output.json`

* [get-records input](./get-records-input.md "Records of a zone, and whether this module may edit them") – `http://schema.nethserver.org/powerdns/get-records-input.json`

* [get-records output](./get-records-output.md "Records of a zone, and whether this module may edit them") – `http://schema.nethserver.org/powerdns/get-records-output.json`

* [get-zone input](./get-zone-input.md "One zone, with DS records on a primary") – `http://schema.nethserver.org/powerdns/get-zone-input.json`

* [get-zone output](./get-zone-output.md "One zone, with what the registrar needs on a primary") – `http://schema.nethserver.org/powerdns/get-zone-output.json`

* [list-secondaries output](./list-secondaries-output.md "Registered secondaries, with replication lag") – `http://schema.nethserver.org/powerdns/list-secondaries-output.json`

* [list-zones output](./list-zones-output.md "Zones served by this instance") – `http://schema.nethserver.org/powerdns/list-zones-output.json`

* [register-secondary input](./register-secondary-input.md "Role replica") – `http://schema.nethserver.org/powerdns/register-secondary-input.json`

* [register-secondary output](./register-secondary-output.md "Role replica") – `http://schema.nethserver.org/powerdns/register-secondary-output.json`

* [remove-secondary input](./remove-secondary-input.md "Remove a stale secondary entry and revoke its key") – `http://schema.nethserver.org/powerdns/remove-secondary-input.json`

* [remove-secondary output](./remove-secondary-output.md "Remove a stale secondary entry and revoke its key") – `http://schema.nethserver.org/powerdns/remove-secondary-output.json`

* [remove-zone input](./remove-zone-input.md "Delete a zone and its keys") – `http://schema.nethserver.org/powerdns/remove-zone-input.json`

* [remove-zone output](./remove-zone-output.md "Delete a zone and its keys") – `http://schema.nethserver.org/powerdns/remove-zone-output.json`

* [set-records input](./set-records-input.md "Each name and type in the input becomes exactly the values given") – `http://schema.nethserver.org/powerdns/set-records-input.json`

* [set-records output](./set-records-output.md "Each name and type in the input becomes exactly the values given") – `http://schema.nethserver.org/powerdns/set-records-output.json`

* [unregister-secondary input](./unregister-secondary-input.md "Role replica") – `http://schema.nethserver.org/powerdns/unregister-secondary-input.json`

* [unregister-secondary output](./unregister-secondary-output.md "Role replica") – `http://schema.nethserver.org/powerdns/unregister-secondary-output.json`

* [update-zone input](./update-zone-input.md "Change DNSSEC settings and SOA overrides of a zone") – `http://schema.nethserver.org/powerdns/update-zone-input.json`

* [update-zone output](./update-zone-output.md "Change DNSSEC settings and SOA overrides of a zone") – `http://schema.nethserver.org/powerdns/update-zone-output.json`

## Other Schemas

### Objects

* [Untitled object in add-zone output](./add-zone-output-properties-glue-items.md) – `http://schema.nethserver.org/powerdns/add-zone-output.json#/properties/glue/items`

* [Untitled object in check-delegation output](./check-delegation-output-properties-glue-items.md) – `http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items`

* [Untitled object in delete-records input](./delete-records-input-properties-records-items.md) – `http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records/items`

* [Untitled object in delete-records output](./delete-records-output-properties-records-items.md) – `http://schema.nethserver.org/powerdns/delete-records-output.json#/properties/records/items`

* [Untitled object in get-configuration output](./get-configuration-output-properties-vpn_port.md) – `http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/vpn_port`

* [Untitled object in get-configuration output](./get-configuration-output-properties-dnshelper.md) – `http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/dnshelper`

* [Untitled object in get-dns-status output](./get-dns-status-output-properties-secondaries-items.md) – `http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/secondaries/items`

* [Untitled object in get-provider-config output](./get-provider-config-output-properties-fields.md) – `http://schema.nethserver.org/powerdns/get-provider-config-output.json#/properties/fields`

* [Untitled object in get-records output](./get-records-output-properties-records-items.md) – `http://schema.nethserver.org/powerdns/get-records-output.json#/properties/records/items`

* [Untitled object in get-zone output](./get-zone-output-properties-name_servers-items.md) – `http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items`

* [Untitled object in get-zone output](./get-zone-output-properties-name_servers-items-properties-addresses-items.md) – `http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/addresses/items`

* [Untitled object in list-secondaries output](./list-secondaries-output-properties-secondaries-items.md) – `http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items`

* [Untitled object in list-zones output](./list-zones-output-properties-zones-items.md) – `http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items`

* [Untitled object in set-records input](./set-records-input-properties-records-items.md) – `http://schema.nethserver.org/powerdns/set-records-input.json#/properties/records/items`

* [Untitled object in set-records output](./set-records-output-properties-records-items.md) – `http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records/items`

* [Untitled object in update-zone output](./update-zone-output-properties-glue-items.md) – `http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/glue/items`

### Arrays

* [Untitled array in add-zone output](./add-zone-output-properties-glue.md "NS names inside the zone: the registrar needs glue for them") – `http://schema.nethserver.org/powerdns/add-zone-output.json#/properties/glue`

* [Untitled array in add-zone output](./add-zone-output-properties-glue-items-properties-addresses.md) – `http://schema.nethserver.org/powerdns/add-zone-output.json#/properties/glue/items/properties/addresses`

* [Untitled array in check-delegation output](./check-delegation-output-properties-ns_expected.md "NS names the registrar should list") – `http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_expected`

* [Untitled array in check-delegation output](./check-delegation-output-properties-ns_missing.md "Expected NS names the parent does not list") – `http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_missing`

* [Untitled array in check-delegation output](./check-delegation-output-properties-ns_extra.md "NS names the parent lists that are not expected") – `http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_extra`

* [Untitled array in check-delegation output](./check-delegation-output-properties-glue.md "For each NS name inside the zone, the glue the parent should publish and does") – `http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue`

* [Untitled array in check-delegation output](./check-delegation-output-properties-glue-items-properties-expected.md) – `http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items/properties/expected`

* [Untitled array in check-delegation output](./check-delegation-output-properties-glue-items-properties-published.md) – `http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items/properties/published`

* [Untitled array in check-delegation output](./check-delegation-output-properties-ds_expected.md "SHA-256 DS records for the zone, empty when unsigned") – `http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ds_expected`

* [Untitled array in configure-module input](./configure-module-input-properties-listen_addresses.md "Node addresses to serve DNS on, besides the cluster VPN address") – `http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/listen_addresses`

* [Untitled array in delete-records input](./delete-records-input-properties-records.md) – `http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records`

* [Untitled array in delete-records output](./delete-records-output-properties-records.md) – `http://schema.nethserver.org/powerdns/delete-records-output.json#/properties/records`

* [Untitled array in get-configuration output](./get-configuration-output-properties-listen_addresses.md) – `http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/listen_addresses`

* [Untitled array in get-configuration output](./get-configuration-output-properties-missing_addresses.md) – `http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/missing_addresses`

* [Untitled array in get-configuration output](./get-configuration-output-properties-node_addresses.md) – `http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/node_addresses`

* [Untitled array in get-configuration output](./get-configuration-output-properties-primaries.md) – `http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/primaries`

* [Untitled array in get-dns-status output](./get-dns-status-output-properties-zones.md) – `http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/zones`

* [Untitled array in get-dns-status output](./get-dns-status-output-properties-secondaries.md) – `http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/secondaries`

* [Untitled array in get-dns-status output](./get-dns-status-output-properties-secondaries-items-properties-zones_behind.md) – `http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/secondaries/items/properties/zones_behind`

* [Untitled array in get-dns-status output](./get-dns-status-output-properties-other_primaries.md) – `http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/other_primaries`

* [Untitled array in get-provider-config output](./get-provider-config-output-properties-zones.md) – `http://schema.nethserver.org/powerdns/get-provider-config-output.json#/properties/zones`

* [Untitled array in get-records output](./get-records-output-properties-records.md) – `http://schema.nethserver.org/powerdns/get-records-output.json#/properties/records`

* [Untitled array in get-zone output](./get-zone-output-properties-ds_records.md "SHA-256 DS records for the registrar") – `http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/ds_records`

* [Untitled array in get-zone output](./get-zone-output-properties-dnskey_records.md "The zone's published DNSKEY records, for registries that ask for the key instead of a DS") – `http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/dnskey_records`

* [Untitled array in get-zone output](./get-zone-output-properties-name_servers.md "On a primary: the NS names to give the registrar, whether each needs glue, and its known addresses") – `http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers`

* [Untitled array in get-zone output](./get-zone-output-properties-name_servers-items-properties-addresses.md) – `http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/addresses`

* [Untitled array in list-secondaries output](./list-secondaries-output-properties-secondaries.md) – `http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries`

* [Untitled array in list-secondaries output](./list-secondaries-output-properties-secondaries-items-properties-zones_behind.md) – `http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/zones_behind`

* [Untitled array in list-zones output](./list-zones-output-properties-zones.md) – `http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones`

* [Untitled array in register-secondary input](./register-secondary-input-properties-addresses.md "Its public addresses, shown as glue") – `http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/addresses`

* [Untitled array in set-records input](./set-records-input-properties-records.md) – `http://schema.nethserver.org/powerdns/set-records-input.json#/properties/records`

* [Untitled array in set-records output](./set-records-output-properties-records.md) – `http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records`

* [Untitled array in update-zone output](./update-zone-output-properties-ds_records.md "SHA-256 DS records for the registrar") – `http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/ds_records`

* [Untitled array in update-zone output](./update-zone-output-properties-glue.md "NS names inside the zone: the registrar needs glue for them") – `http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/glue`

* [Untitled array in update-zone output](./update-zone-output-properties-glue-items-properties-addresses.md) – `http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/glue/items/properties/addresses`

## Version Note

The schemas linked above follow the JSON Schema Spec version: `http://json-schema.org/draft-07/schema#`
