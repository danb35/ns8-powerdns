# Untitled object in set-records output Schema

```txt
http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                           |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [set-records-output.json\*](powerdns/set-records-output.json "open original schema") |

## items Type

`object` ([Details](set-records-output-properties-records-items.md))

# items Properties

| Property      | Type      | Required | Nullable       | Defined by                                                                                                                                                                                     |
| :------------ | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name) | `string`  | Required | cannot be null | [set-records output](set-records-output-properties-records-items-properties-name.md "http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records/items/properties/name") |
| [type](#type) | `string`  | Required | cannot be null | [set-records output](set-records-output-properties-records-items-properties-type.md "http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records/items/properties/type") |
| [ttl](#ttl)   | `integer` | Required | cannot be null | [set-records output](set-records-output-properties-records-items-properties-ttl.md "http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records/items/properties/ttl")   |
| [data](#data) | `string`  | Required | cannot be null | [set-records output](set-records-output-properties-records-items-properties-data.md "http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records/items/properties/data") |

## name

Name relative to the zone, '@' for the apex

`name`

* is required

* Type: `string`

* cannot be null

* defined in: [set-records output](set-records-output-properties-records-items-properties-name.md "http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records/items/properties/name")

### name Type

`string`

### name Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## type



`type`

* is required

* Type: `string`

* cannot be null

* defined in: [set-records output](set-records-output-properties-records-items-properties-type.md "http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records/items/properties/type")

### type Type

`string`

### type Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[A-Za-z0-9]+$
```

[try pattern](https://regexr.com/?expression=%5E%5BA-Za-z0-9%5D%2B%24 "try regular expression with regexr.com")

## ttl

Seconds; 0 or absent keeps 3600

`ttl`

* is required

* Type: `integer`

* cannot be null

* defined in: [set-records output](set-records-output-properties-records-items-properties-ttl.md "http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records/items/properties/ttl")

### ttl Type

`integer`

### ttl Constraints

**minimum**: the value of this number must greater than or equal to: `0`

## data

RDATA in unescaped zone-file syntax. TXT: the whole plain value, unquoted

`data`

* is required

* Type: `string`

* cannot be null

* defined in: [set-records output](set-records-output-properties-records-items-properties-data.md "http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records/items/properties/data")

### data Type

`string`
