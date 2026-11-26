# Untitled object in update-external-secondary output Schema

```txt
http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                                       |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [update-external-secondary-output.json\*](powerdns/update-external-secondary-output.json "open original schema") |

## secondary Type

`object` ([Details](update-external-secondary-output-properties-secondary.md))

# secondary Properties

| Property                        | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                                         |
| :------------------------------ | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](#id)                       | `string`  | Required | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-id.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/id")                       |
| [name](#name)                   | `string`  | Required | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-name.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/name")                   |
| [notify](#notify)               | `array`   | Required | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-notify.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/notify")               |
| [auth](#auth)                   | `string`  | Required | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-auth.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/auth")                   |
| [tsig_key](#tsig_key)           | `string`  | Required | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-tsig_key.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/tsig_key")           |
| [transfer_from](#transfer_from) | `array`   | Required | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-transfer_from.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/transfer_from") |
| [ns_names](#ns_names)           | `array`   | Required | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-ns_names.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/ns_names")           |
| [advertise](#advertise)         | `boolean` | Required | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-advertise.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/advertise")         |
| [zones](#zones)                 | Merged    | Required | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-zones.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/zones")                 |

## id



`id`

* is required

* Type: `string`

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-id.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/id")

### id Type

`string`

## name



`name`

* is required

* Type: `string`

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-name.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/name")

### name Type

`string`

## notify



`notify`

* is required

* Type: `string[]`

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-notify.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/notify")

### notify Type

`string[]`

## auth



`auth`

* is required

* Type: `string`

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-auth.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/auth")

### auth Type

`string`

## tsig_key



`tsig_key`

* is required

* Type: `string`

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-tsig_key.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/tsig_key")

### tsig_key Type

`string`

## transfer_from



`transfer_from`

* is required

* Type: `string[]`

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-transfer_from.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/transfer_from")

### transfer_from Type

`string[]`

## ns_names



`ns_names`

* is required

* Type: `string[]`

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-ns_names.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/ns_names")

### ns_names Type

`string[]`

## advertise



`advertise`

* is required

* Type: `boolean`

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-advertise.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/advertise")

### advertise Type

`boolean`

## zones



`zones`

* is required

* Type: merged type ([Details](update-external-secondary-output-properties-secondary-properties-zones.md))

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-secondary-properties-zones.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary/properties/zones")

### zones Type

merged type ([Details](update-external-secondary-output-properties-secondary-properties-zones.md))

one (and only one) of

* [Untitled string in update-external-secondary output](update-external-secondary-output-properties-secondary-properties-zones-oneof-0.md "check type definition")

* [Untitled array in update-external-secondary output](update-external-secondary-output-properties-secondary-properties-zones-oneof-1.md "check type definition")
