# Untitled object in list-secondaries output Schema

```txt
http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [list-secondaries-output.json\*](powerdns/list-secondaries-output.json "open original schema") |

## items Type

`object` ([Details](list-secondaries-output-properties-secondaries-items.md))

# items Properties

| Property                      | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                            |
| :---------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [module_id](#module_id)       | `string`  | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-module_id.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/module_id")       |
| [address](#address)           | `string`  | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-address.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/address")           |
| [ns_name](#ns_name)           | `string`  | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-ns_name.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/ns_name")           |
| [advertise](#advertise)       | `boolean` | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-advertise.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/advertise")       |
| [reachable](#reachable)       | `boolean` | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-reachable.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/reachable")       |
| [zones_total](#zones_total)   | `integer` | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-zones_total.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/zones_total")   |
| [zones_behind](#zones_behind) | `array`   | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-zones_behind.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/zones_behind") |

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-module_id.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/module_id")

### module_id Type

`string`

## address



`address`

* is required

* Type: `string`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-address.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/address")

### address Type

`string`

## ns_name



`ns_name`

* is required

* Type: `string`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-ns_name.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/ns_name")

### ns_name Type

`string`

## advertise



`advertise`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-advertise.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/advertise")

### advertise Type

`boolean`

## reachable



`reachable`

* is required

* Type: `boolean`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-reachable.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/reachable")

### reachable Type

`boolean`

## zones_total



`zones_total`

* is required

* Type: `integer`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-zones_total.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/zones_total")

### zones_total Type

`integer`

## zones_behind



`zones_behind`

* is required

* Type: `string[]`

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-secondaries-items-properties-zones_behind.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries/items/properties/zones_behind")

### zones_behind Type

`string[]`
