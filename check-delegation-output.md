# check-delegation output Schema

```txt
http://schema.nethserver.org/powerdns/check-delegation-output.json
```

Compare what the parent zone publishes for a zone with what the zone needs at the registrar. Informational

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [check-delegation-output.json](powerdns/check-delegation-output.json "open original schema") |

## check-delegation output Type

`object` ([check-delegation output](check-delegation-output.md))

## check-delegation output Examples

```json
{
  "zone": "example.com",
  "resolver": "1.1.1.1",
  "parent": "com",
  "parent_server": "a.gtld-servers.net",
  "delegated": true,
  "ns_expected": [
    "ns1.example.com"
  ],
  "ns_published": [
    "ns1.example.com"
  ],
  "ns_missing": [],
  "ns_extra": [],
  "glue": [
    {
      "ns_name": "ns1.example.com",
      "expected": [
        "192.0.2.1"
      ],
      "published": [
        "192.0.2.1"
      ],
      "ok": true
    }
  ],
  "signed": true,
  "ds_expected": [
    "12345 13 2 ABCDEF"
  ],
  "ds_published": [
    "12345 13 2 ABCDEF"
  ],
  "ds_ok": true,
  "resolution": "ok"
}
```

# check-delegation output Properties

| Property                        | Type      | Required | Nullable       | Defined by                                                                                                                                                                    |
| :------------------------------ | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone)                   | `string`  | Required | cannot be null | [check-delegation output](check-delegation-output-properties-zone.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/zone")                   |
| [resolver](#resolver)           | `string`  | Required | cannot be null | [check-delegation output](check-delegation-output-properties-resolver.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/resolver")           |
| [parent](#parent)               | `string`  | Required | cannot be null | [check-delegation output](check-delegation-output-properties-parent.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/parent")               |
| [parent_server](#parent_server) | `string`  | Required | cannot be null | [check-delegation output](check-delegation-output-properties-parent_server.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/parent_server") |
| [delegated](#delegated)         | `boolean` | Required | can be null    | [check-delegation output](check-delegation-output-properties-delegated.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/delegated")         |
| [ns_expected](#ns_expected)     | `array`   | Required | cannot be null | [check-delegation output](check-delegation-output-properties-ns_expected.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_expected")     |
| [ns_published](#ns_published)   | `array`   | Required | can be null    | [check-delegation output](check-delegation-output-properties-ns_published.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_published")   |
| [ns_missing](#ns_missing)       | `array`   | Required | cannot be null | [check-delegation output](check-delegation-output-properties-ns_missing.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_missing")       |
| [ns_extra](#ns_extra)           | `array`   | Required | cannot be null | [check-delegation output](check-delegation-output-properties-ns_extra.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_extra")           |
| [glue](#glue)                   | `array`   | Required | cannot be null | [check-delegation output](check-delegation-output-properties-glue.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue")                   |
| [signed](#signed)               | `boolean` | Required | cannot be null | [check-delegation output](check-delegation-output-properties-signed.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/signed")               |
| [ds_expected](#ds_expected)     | `array`   | Required | cannot be null | [check-delegation output](check-delegation-output-properties-ds_expected.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ds_expected")     |
| [ds_published](#ds_published)   | `array`   | Required | can be null    | [check-delegation output](check-delegation-output-properties-ds_published.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ds_published")   |
| [ds_ok](#ds_ok)                 | `boolean` | Required | can be null    | [check-delegation output](check-delegation-output-properties-ds_ok.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ds_ok")                 |
| [resolution](#resolution)       | `string`  | Required | can be null    | [check-delegation output](check-delegation-output-properties-resolution.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/resolution")       |

## zone



`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-zone.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/zone")

### zone Type

`string`

## resolver

The public resolver used; empty when none answered

`resolver`

* is required

* Type: `string`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-resolver.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/resolver")

### resolver Type

`string`

## parent

The enclosing zone that delegates this one, like com

`parent`

* is required

* Type: `string`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-parent.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/parent")

### parent Type

`string`

## parent_server

The parent name server that was asked

`parent_server`

* is required

* Type: `string`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-parent_server.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/parent_server")

### parent_server Type

`string`

## delegated

Whether the parent delegates the zone at all; null when no parent server answered

`delegated`

* is required

* Type: `boolean`

* can be null

* defined in: [check-delegation output](check-delegation-output-properties-delegated.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/delegated")

### delegated Type

`boolean`

## ns_expected

NS names the registrar should list

`ns_expected`

* is required

* Type: `string[]`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-ns_expected.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_expected")

### ns_expected Type

`string[]`

## ns_published

NS names the parent lists

`ns_published`

* is required

* Type: `string[]`

* can be null

* defined in: [check-delegation output](check-delegation-output-properties-ns_published.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_published")

### ns_published Type

`string[]`

## ns_missing

Expected NS names the parent does not list

`ns_missing`

* is required

* Type: `string[]`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-ns_missing.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_missing")

### ns_missing Type

`string[]`

## ns_extra

NS names the parent lists that are not expected

`ns_extra`

* is required

* Type: `string[]`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-ns_extra.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ns_extra")

### ns_extra Type

`string[]`

## glue

For each NS name inside the zone, the glue the parent should publish and does

`glue`

* is required

* Type: `object[]` ([Details](check-delegation-output-properties-glue-items.md))

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-glue.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue")

### glue Type

`object[]` ([Details](check-delegation-output-properties-glue-items.md))

## signed



`signed`

* is required

* Type: `boolean`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-signed.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/signed")

### signed Type

`boolean`

## ds_expected

SHA-256 DS records for the zone, empty when unsigned

`ds_expected`

* is required

* Type: `string[]`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-ds_expected.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ds_expected")

### ds_expected Type

`string[]`

## ds_published

DS records at the parent; null when the resolver did not answer

`ds_published`

* is required

* Type: `string[]`

* can be null

* defined in: [check-delegation output](check-delegation-output-properties-ds_published.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ds_published")

### ds_published Type

`string[]`

## ds_ok

Signed: every DS at the parent matches a key. Unsigned: the parent has no DS

`ds_ok`

* is required

* Type: `boolean`

* can be null

* defined in: [check-delegation output](check-delegation-output-properties-ds_ok.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/ds_ok")

### ds_ok Type

`boolean`

## resolution

How a validating resolver answers the zone SOA

`resolution`

* is required

* Type: `string`

* can be null

* defined in: [check-delegation output](check-delegation-output-properties-resolution.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/resolution")

### resolution Type

`string`

### resolution Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value        | Explanation |    |    |
| :----------- | :---------- | :- | :- |
| `"ok"`       |             |
| `"servfail"` |             |
| `"nxdomain"` |             |
| `"error"`    |             |
| `null`       |             |
