# Untitled object in list-secondaries output Schema

```txt
http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-secondaries-output.json\*](powerdns/list-secondaries-output.json "open original schema") |

## items Type

`object` ([Details](list-secondaries-output-properties-external-items.md))

# items Properties

| Property                        | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                        |
| :------------------------------ | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](#id)                       | `string`  | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-id.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/id")                       |
| [name](#name)                   | `string`  | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-name.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/name")                   |
| [notify](#notify)               | `array`   | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-notify.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/notify")               |
| [auth](#auth)                   | `string`  | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-auth.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/auth")                   |
| [tsig_key](#tsig_key)           | `string`  | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-tsig_key.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/tsig_key")           |
| [transfer_from](#transfer_from) | `array`   | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-transfer_from.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/transfer_from") |
| [ns_names](#ns_names)           | `array`   | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-ns_names.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/ns_names")           |
| [advertise](#advertise)         | `boolean` | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-advertise.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/advertise")         |
| [zones](#zones)                 | Merged    | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-zones.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/zones")                 |
| [answering](#answering)         | `boolean` | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-answering.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/answering")         |
| [zones_total](#zones_total)     | `integer` | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-zones_total.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/zones_total")     |
| [zones_behind](#zones_behind)   | `array`   | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external-items-properties-zones_behind.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/zones_behind")   |

## id



`id`

* is required

* Type: `string`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-id.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/id")

### id Type

`string`

## name



`name`

* is required

* Type: `string`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-name.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/name")

### name Type

`string`

## notify



`notify`

* is required

* Type: `string[]`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-notify.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/notify")

### notify Type

`string[]`

## auth



`auth`

* is required

* Type: `string`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-auth.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/auth")

### auth Type

`string`

## tsig_key



`tsig_key`

* is required

* Type: `string`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-tsig_key.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/tsig_key")

### tsig_key Type

`string`

## transfer_from



`transfer_from`

* is required

* Type: `string[]`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-transfer_from.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/transfer_from")

### transfer_from Type

`string[]`

## ns_names



`ns_names`

* is required

* Type: `string[]`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-ns_names.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/ns_names")

### ns_names Type

`string[]`

## advertise



`advertise`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-advertise.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/advertise")

### advertise Type

`boolean`

## zones



`zones`

* is required

* Type: merged type ([Details](list-secondaries-output-properties-external-items-properties-zones.md))

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-zones.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/zones")

### zones Type

merged type ([Details](list-secondaries-output-properties-external-items-properties-zones.md))

one (and only one) of

* [Untitled string in list-secondaries output](list-secondaries-output-properties-external-items-properties-zones-oneof-0.md "check type definition")

* [Untitled array in list-secondaries output](list-secondaries-output-properties-external-items-properties-zones-oneof-1.md "check type definition")

## answering



`answering`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-answering.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/answering")

### answering Type

`boolean`

## zones_total



`zones_total`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-zones_total.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/zones_total")

### zones_total Type

`integer`

## zones_behind



`zones_behind`

* is required

* Type: `string[]`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external-items-properties-zones_behind.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external/items/properties/zones_behind")

### zones_behind Type

`string[]`
