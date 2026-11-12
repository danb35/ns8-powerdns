# update-external-secondary input Schema

```txt
http://schema.nethserver.org/powerdns/update-external-secondary-input.json
```

Change a secondary outside the cluster; fields left out keep their value

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [update-external-secondary-input.json](powerdns/update-external-secondary-input.json "open original schema") |

## update-external-secondary input Type

`object` ([update-external-secondary input](update-external-secondary-input.md))

# update-external-secondary input Properties

| Property                        | Type      | Required | Nullable       | Defined by                                                                                                                                                                                            |
| :------------------------------ | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [id](#id)                       | `string`  | Required | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-id.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/id")                       |
| [name](#name)                   | `string`  | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-name.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/name")                   |
| [notify](#notify)               | `array`   | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-notify.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/notify")               |
| [auth](#auth)                   | `string`  | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-auth.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/auth")                   |
| [transfer_from](#transfer_from) | `array`   | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-transfer_from.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/transfer_from") |
| [ns_names](#ns_names)           | `array`   | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-ns_names.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/ns_names")           |
| [advertise](#advertise)         | `boolean` | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-advertise.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/advertise")         |
| [zones](#zones)                 | Merged    | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-zones.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/zones")                 |
| [tsig](#tsig)                   | `object`  | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-tsig.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig")                   |

## id



`id`

* is required

* Type: `string`

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-id.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/id")

### id Type

`string`

### id Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## name

A label for the UI

`name`

* is optional

* Type: `string`

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-name.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/name")

### name Type

`string`

### name Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## notify

Addresses to send NOTIFY to

`notify`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-notify.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/notify")

### notify Type

`string[]`

### notify Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## auth

TSIG key (default), or source addresses only

`auth`

* is optional

* Type: `string`

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-auth.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/auth")

### auth Type

`string`

### auth Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |    |    |
| :------- | :---------- | :- | :- |
| `"tsig"` |             |
| `"ip"`   |             |

## transfer_from

With auth ip: the addresses or networks the peer transfers from

`transfer_from`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-transfer_from.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/transfer_from")

### transfer_from Type

`string[]`

## ns_names

The peer's name servers

`ns_names`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-ns_names.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/ns_names")

### ns_names Type

`string[]`

## advertise

List ns_names in the apex NS of the zones it receives

`advertise`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-advertise.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/advertise")

### advertise Type

`boolean`

## zones

all, including zones added later, or a list of zones

`zones`

* is optional

* Type: merged type ([Details](update-external-secondary-input-properties-zones.md))

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-zones.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/zones")

### zones Type

merged type ([Details](update-external-secondary-input-properties-zones.md))

one (and only one) of

* [Untitled string in update-external-secondary input](update-external-secondary-input-properties-zones-oneof-0.md "check type definition")

* [Untitled array in update-external-secondary input](update-external-secondary-input-properties-zones-oneof-1.md "check type definition")

## tsig



`tsig`

* is optional

* Type: `object` ([Details](update-external-secondary-input-properties-tsig.md))

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-tsig.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig")

### tsig Type

`object` ([Details](update-external-secondary-input-properties-tsig.md))
