# get-configuration output Schema

```txt
http://schema.nethserver.org/powerdns/get-configuration-output.json
```

Current configuration, node addresses with port 53 availability, the primary if any, and dnshelper

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-configuration-output.json](powerdns/get-configuration-output.json "open original schema") |

## get-configuration output Type

`object` ([get-configuration output](get-configuration-output.md))

# get-configuration output Properties

| Property                                | Type      | Required | Nullable       | Defined by                                                                                                                                                                               |
| :-------------------------------------- | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [configured](#configured)               | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-configured.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/configured")               |
| [role](#role)                           | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-role.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/role")                           |
| [ns_name](#ns_name)                     | `string`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-ns_name.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/ns_name")                     |
| [advertise](#advertise)                 | `boolean` | Required | cannot be null | [get-configuration output](get-configuration-output-properties-advertise.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/advertise")                 |
| [listen_addresses](#listen_addresses)   | `array`   | Required | cannot be null | [get-configuration output](get-configuration-output-properties-listen_addresses.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/listen_addresses")   |
| [missing_addresses](#missing_addresses) | `array`   | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-missing_addresses.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/missing_addresses") |
| [hostmaster](#hostmaster)               | `string`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-hostmaster.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/hostmaster")               |
| [soa_refresh](#soa_refresh)             | `integer` | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-soa_refresh.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/soa_refresh")             |
| [soa_retry](#soa_retry)                 | `integer` | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-soa_retry.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/soa_retry")                 |
| [soa_expire](#soa_expire)               | `integer` | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-soa_expire.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/soa_expire")               |
| [soa_minimum](#soa_minimum)             | `integer` | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-soa_minimum.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/soa_minimum")             |
| [primary](#primary)                     | `string`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-primary.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/primary")                     |
| [vpn_address](#vpn_address)             | `string`  | Optional | can be null    | [get-configuration output](get-configuration-output-properties-vpn_address.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/vpn_address")             |
| [standby](#standby)                     | `boolean` | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-standby.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/standby")                     |
| [node_addresses](#node_addresses)       | `array`   | Required | cannot be null | [get-configuration output](get-configuration-output-properties-node_addresses.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/node_addresses")       |
| [vpn_port](#vpn_port)                   | `object`  | Optional | cannot be null | [get-configuration output](get-configuration-output-properties-vpn_port.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/vpn_port")                   |
| [primaries](#primaries)                 | `array`   | Required | cannot be null | [get-configuration output](get-configuration-output-properties-primaries.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/primaries")                 |
| [dnshelper](#dnshelper)                 | `object`  | Required | cannot be null | [get-configuration output](get-configuration-output-properties-dnshelper.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/dnshelper")                 |

## configured



`configured`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-configured.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/configured")

### configured Type

`boolean`

## role



`role`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-role.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/role")

### role Type

`string`

## ns_name



`ns_name`

* is required

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-ns_name.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/ns_name")

### ns_name Type

`string`

## advertise



`advertise`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-advertise.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/advertise")

### advertise Type

`boolean`

## listen_addresses



`listen_addresses`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-listen_addresses.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/listen_addresses")

### listen_addresses Type

`string[]`

## missing_addresses



`missing_addresses`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-missing_addresses.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/missing_addresses")

### missing_addresses Type

`string[]`

## hostmaster



`hostmaster`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-hostmaster.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/hostmaster")

### hostmaster Type

`string`

## soa_refresh



`soa_refresh`

* is optional

* Type: `integer`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-soa_refresh.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/soa_refresh")

### soa_refresh Type

`integer`

### soa_refresh Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## soa_retry



`soa_retry`

* is optional

* Type: `integer`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-soa_retry.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/soa_retry")

### soa_retry Type

`integer`

### soa_retry Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## soa_expire



`soa_expire`

* is optional

* Type: `integer`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-soa_expire.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/soa_expire")

### soa_expire Type

`integer`

### soa_expire Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## soa_minimum



`soa_minimum`

* is optional

* Type: `integer`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-soa_minimum.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/soa_minimum")

### soa_minimum Type

`integer`

### soa_minimum Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## primary



`primary`

* is optional

* Type: `string`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-primary.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/primary")

### primary Type

`string`

## vpn_address



`vpn_address`

* is optional

* Type: `string`

* can be null

* defined in: [get-configuration output](get-configuration-output-properties-vpn_address.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/vpn_address")

### vpn_address Type

`string`

## standby



`standby`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-standby.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/standby")

### standby Type

`boolean`

## node_addresses



`node_addresses`

* is required

* Type: `array`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-node_addresses.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/node_addresses")

### node_addresses Type

`array`

## vpn_port



`vpn_port`

* is optional

* Type: `object` ([Details](get-configuration-output-properties-vpn_port.md))

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-vpn_port.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/vpn_port")

### vpn_port Type

`object` ([Details](get-configuration-output-properties-vpn_port.md))

## primaries



`primaries`

* is required

* Type: `array`

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-primaries.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/primaries")

### primaries Type

`array`

## dnshelper



`dnshelper`

* is required

* Type: `object` ([Details](get-configuration-output-properties-dnshelper.md))

* cannot be null

* defined in: [get-configuration output](get-configuration-output-properties-dnshelper.md "http://schema.nethserver.org/powerdns/get-configuration-output.json#/properties/dnshelper")

### dnshelper Type

`object` ([Details](get-configuration-output-properties-dnshelper.md))
