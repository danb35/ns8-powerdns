# Untitled object in get-zone output Schema

```txt
http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-zone-output.json\*](powerdns/get-zone-output.json "open original schema") |

## items Type

`object` ([Details](get-zone-output-properties-name_servers-items.md))

# items Properties

| Property                | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                |
| :---------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ns_name](#ns_name)     | `string`  | Required | cannot be null | [get-zone output](get-zone-output-properties-name_servers-items-properties-ns_name.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/ns_name")     |
| [glue](#glue)           | `boolean` | Required | cannot be null | [get-zone output](get-zone-output-properties-name_servers-items-properties-glue.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/glue")           |
| [external](#external)   | `boolean` | Optional | cannot be null | [get-zone output](get-zone-output-properties-name_servers-items-properties-external.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/external")   |
| [addresses](#addresses) | `array`   | Required | cannot be null | [get-zone output](get-zone-output-properties-name_servers-items-properties-addresses.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/addresses") |

## ns_name



`ns_name`

* is required

* Type: `string`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-name_servers-items-properties-ns_name.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/ns_name")

### ns_name Type

`string`

## glue

The name lies inside the zone, so the registrar needs its addresses

`glue`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-name_servers-items-properties-glue.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/glue")

### glue Type

`boolean`

## external

An external secondary's name server: its addresses come from the provider

`external`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-name_servers-items-properties-external.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/external")

### external Type

`boolean`

## addresses



`addresses`

* is required

* Type: `object[]` ([Details](get-zone-output-properties-name_servers-items-properties-addresses-items.md))

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-name_servers-items-properties-addresses.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/addresses")

### addresses Type

`object[]` ([Details](get-zone-output-properties-name_servers-items-properties-addresses-items.md))
