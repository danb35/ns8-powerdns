# get-dns-status output Schema

```txt
http://schema.nethserver.org/powerdns/get-dns-status-output.json
```

Per-zone serials, replication lag and standby state, for the Status page

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                               |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-dns-status-output.json](powerdns/get-dns-status-output.json "open original schema") |

## get-dns-status output Type

`object` ([get-dns-status output](get-dns-status-output.md))

# get-dns-status output Properties

| Property                                | Type      | Required | Nullable       | Defined by                                                                                                                                                                      |
| :-------------------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [role](#role)                           | `string`  | Required | cannot be null | [get-dns-status output](get-dns-status-output-properties-role.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/role")                           |
| [configured](#configured)               | `boolean` | Required | cannot be null | [get-dns-status output](get-dns-status-output-properties-configured.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/configured")               |
| [standby](#standby)                     | `boolean` | Required | cannot be null | [get-dns-status output](get-dns-status-output-properties-standby.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/standby")                     |
| [service_active](#service_active)       | `boolean` | Required | cannot be null | [get-dns-status output](get-dns-status-output-properties-service_active.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/service_active")       |
| [api_ready](#api_ready)                 | `boolean` | Required | cannot be null | [get-dns-status output](get-dns-status-output-properties-api_ready.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/api_ready")                 |
| [zones](#zones)                         | `array`   | Required | cannot be null | [get-dns-status output](get-dns-status-output-properties-zones.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/zones")                         |
| [secondaries](#secondaries)             | `array`   | Required | cannot be null | [get-dns-status output](get-dns-status-output-properties-secondaries.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/secondaries")             |
| [other_primaries](#other_primaries)     | `array`   | Required | cannot be null | [get-dns-status output](get-dns-status-output-properties-other_primaries.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/other_primaries")     |
| [primary_reachable](#primary_reachable) | `boolean` | Optional | can be null    | [get-dns-status output](get-dns-status-output-properties-primary_reachable.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/primary_reachable") |

## role



`role`

* is required

* Type: `string`

* cannot be null

* defined in: [get-dns-status output](get-dns-status-output-properties-role.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/role")

### role Type

`string`

## configured



`configured`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-dns-status output](get-dns-status-output-properties-configured.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/configured")

### configured Type

`boolean`

## standby



`standby`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-dns-status output](get-dns-status-output-properties-standby.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/standby")

### standby Type

`boolean`

## service_active



`service_active`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-dns-status output](get-dns-status-output-properties-service_active.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/service_active")

### service_active Type

`boolean`

## api_ready



`api_ready`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-dns-status output](get-dns-status-output-properties-api_ready.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/api_ready")

### api_ready Type

`boolean`

## zones



`zones`

* is required

* Type: `array`

* cannot be null

* defined in: [get-dns-status output](get-dns-status-output-properties-zones.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/zones")

### zones Type

`array`

## secondaries



`secondaries`

* is required

* Type: `object[]` ([Details](get-dns-status-output-properties-secondaries-items.md))

* cannot be null

* defined in: [get-dns-status output](get-dns-status-output-properties-secondaries.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/secondaries")

### secondaries Type

`object[]` ([Details](get-dns-status-output-properties-secondaries-items.md))

## other_primaries



`other_primaries`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-dns-status output](get-dns-status-output-properties-other_primaries.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/other_primaries")

### other_primaries Type

`string[]`

## primary_reachable



`primary_reachable`

* is optional

* Type: `boolean`

* can be null

* defined in: [get-dns-status output](get-dns-status-output-properties-primary_reachable.md "http://schema.nethserver.org/powerdns/get-dns-status-output.json#/properties/primary_reachable")

### primary_reachable Type

`boolean`
