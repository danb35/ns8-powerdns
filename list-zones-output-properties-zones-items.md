# Untitled object in list-zones output Schema

```txt
http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-zones-output.json\*](powerdns/list-zones-output.json "open original schema") |

## items Type

`object` ([Details](list-zones-output-properties-zones-items.md))

# items Properties

| Property                    | Type      | Required | Nullable       | Defined by                                                                                                                                                                                            |
| :-------------------------- | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone)               | `string`  | Required | cannot be null | [list-zones output](list-zones-output-properties-zones-items-properties-zone.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/zone")               |
| [kind](#kind)               | `string`  | Required | cannot be null | [list-zones output](list-zones-output-properties-zones-items-properties-kind.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/kind")               |
| [serial](#serial)           | `integer` | Required | cannot be null | [list-zones output](list-zones-output-properties-zones-items-properties-serial.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/serial")           |
| [dnssec](#dnssec)           | `boolean` | Required | cannot be null | [list-zones output](list-zones-output-properties-zones-items-properties-dnssec.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/dnssec")           |
| [last_check](#last_check)   | `integer` | Optional | cannot be null | [list-zones output](list-zones-output-properties-zones-items-properties-last_check.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/last_check")   |
| [transferred](#transferred) | `boolean` | Optional | cannot be null | [list-zones output](list-zones-output-properties-zones-items-properties-transferred.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/transferred") |

## zone



`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [list-zones output](list-zones-output-properties-zones-items-properties-zone.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/zone")

### zone Type

`string`

## kind



`kind`

* is required

* Type: `string`

* cannot be null

* defined in: [list-zones output](list-zones-output-properties-zones-items-properties-kind.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/kind")

### kind Type

`string`

## serial



`serial`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-zones output](list-zones-output-properties-zones-items-properties-serial.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/serial")

### serial Type

`integer`

## dnssec



`dnssec`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-zones output](list-zones-output-properties-zones-items-properties-dnssec.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/dnssec")

### dnssec Type

`boolean`

## last_check



`last_check`

* is optional

* Type: `integer`

* cannot be null

* defined in: [list-zones output](list-zones-output-properties-zones-items-properties-last_check.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/last_check")

### last_check Type

`integer`

## transferred



`transferred`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [list-zones output](list-zones-output-properties-zones-items-properties-transferred.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones/items/properties/transferred")

### transferred Type

`boolean`
