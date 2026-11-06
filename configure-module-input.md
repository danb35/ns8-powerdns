# configure-module input Schema

```txt
http://schema.nethserver.org/powerdns/configure-module-input.json
```

Configure the instance as the cluster's primary or as a secondary

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                 |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [configure-module-input.json](powerdns/configure-module-input.json "open original schema") |

## configure-module input Type

`object` ([configure-module input](configure-module-input.md))

# configure-module input Properties

| Property                              | Type      | Required | Nullable       | Defined by                                                                                                                                                                       |
| :------------------------------------ | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [role](#role)                         | `string`  | Required | cannot be null | [configure-module input](configure-module-input-properties-role.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/role")                         |
| [ns_name](#ns_name)                   | `string`  | Required | cannot be null | [configure-module input](configure-module-input-properties-ns_name.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/ns_name")                   |
| [advertise](#advertise)               | `boolean` | Optional | cannot be null | [configure-module input](configure-module-input-properties-advertise.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/advertise")               |
| [listen_addresses](#listen_addresses) | `array`   | Optional | cannot be null | [configure-module input](configure-module-input-properties-listen_addresses.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/listen_addresses") |
| [hostmaster](#hostmaster)             | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-hostmaster.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/hostmaster")             |
| [primary](#primary)                   | `string`  | Optional | cannot be null | [configure-module input](configure-module-input-properties-primary.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/primary")                   |
| [soa_refresh](#soa_refresh)           | `integer` | Optional | cannot be null | [configure-module input](configure-module-input-properties-soa_refresh.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/soa_refresh")           |
| [soa_retry](#soa_retry)               | `integer` | Optional | cannot be null | [configure-module input](configure-module-input-properties-soa_retry.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/soa_retry")               |
| [soa_expire](#soa_expire)             | `integer` | Optional | cannot be null | [configure-module input](configure-module-input-properties-soa_expire.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/soa_expire")             |
| [soa_minimum](#soa_minimum)           | `integer` | Optional | cannot be null | [configure-module input](configure-module-input-properties-soa_minimum.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/soa_minimum")           |

## role

Fixed after the first configuration

`role`

* is required

* Type: `string`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-role.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/role")

### role Type

`string`

### role Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value         | Explanation |    |    |
| :------------ | :---------- | :- | :- |
| `"primary"`   |             |
| `"secondary"` |             |

## ns_name

Public host name this instance answers as

`ns_name`

* is required

* Type: `string`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-ns_name.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/ns_name")

### ns_name Type

`string`

### ns_name Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## advertise

List this instance in the apex NS of every zone

`advertise`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-advertise.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/advertise")

### advertise Type

`boolean`

## listen_addresses

Node addresses to serve DNS on, besides the cluster VPN address

`listen_addresses`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-listen_addresses.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/listen_addresses")

### listen_addresses Type

`string[]`

## hostmaster

SOA contact; required on a primary

`hostmaster`

* is optional

* Type: `string`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-hostmaster.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/hostmaster")

### hostmaster Type

`string`

## primary

Module UUID of the primary to follow; required on a secondary

`primary`

* is optional

* Type: `string`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-primary.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/primary")

### primary Type

`string`

## soa_refresh



`soa_refresh`

* is optional

* Type: `integer`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-soa_refresh.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/soa_refresh")

### soa_refresh Type

`integer`

### soa_refresh Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## soa_retry



`soa_retry`

* is optional

* Type: `integer`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-soa_retry.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/soa_retry")

### soa_retry Type

`integer`

### soa_retry Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## soa_expire



`soa_expire`

* is optional

* Type: `integer`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-soa_expire.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/soa_expire")

### soa_expire Type

`integer`

### soa_expire Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## soa_minimum



`soa_minimum`

* is optional

* Type: `integer`

* cannot be null

* defined in: [configure-module input](configure-module-input-properties-soa_minimum.md "http://schema.nethserver.org/powerdns/configure-module-input.json#/properties/soa_minimum")

### soa_minimum Type

`integer`

### soa_minimum Constraints

**minimum**: the value of this number must greater than or equal to: `1`
