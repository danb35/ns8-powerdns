# Untitled object in delete-records input Schema

```txt
http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                               |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [delete-records-input.json\*](powerdns/delete-records-input.json "open original schema") |

## items Type

`object` ([Details](delete-records-input-properties-records-items.md))

# items Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                                                                                           |
| :------------ | :------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name) | `string` | Required | cannot be null | [delete-records input](delete-records-input-properties-records-items-properties-name.md "http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records/items/properties/name") |
| [type](#type) | `string` | Required | cannot be null | [delete-records input](delete-records-input-properties-records-items-properties-type.md "http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records/items/properties/type") |
| [data](#data) | `string` | Optional | cannot be null | [delete-records input](delete-records-input-properties-records-items-properties-data.md "http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records/items/properties/data") |

## name

Name relative to the zone, '@' for the apex

`name`

* is required

* Type: `string`

* cannot be null

* defined in: [delete-records input](delete-records-input-properties-records-items-properties-name.md "http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records/items/properties/name")

### name Type

`string`

### name Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## type



`type`

* is required

* Type: `string`

* cannot be null

* defined in: [delete-records input](delete-records-input-properties-records-items-properties-type.md "http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records/items/properties/type")

### type Type

`string`

### type Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[A-Za-z0-9]+$
```

[try pattern](https://regexr.com/?expression=%5E%5BA-Za-z0-9%5D%2B%24 "try regular expression with regexr.com")

## data

Delete only this value; absent deletes the whole RRset

`data`

* is optional

* Type: `string`

* cannot be null

* defined in: [delete-records input](delete-records-input-properties-records-items-properties-data.md "http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records/items/properties/data")

### data Type

`string`
