# Untitled object in update-zone output Schema

```txt
http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/glue/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                           |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [update-zone-output.json\*](powerdns/update-zone-output.json "open original schema") |

## items Type

`object` ([Details](update-zone-output-properties-glue-items.md))

# items Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                                                                         |
| :---------------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ns_name](#ns_name)     | `string` | Required | cannot be null | [update-zone output](update-zone-output-properties-glue-items-properties-ns_name.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/glue/items/properties/ns_name")     |
| [addresses](#addresses) | `array`  | Required | cannot be null | [update-zone output](update-zone-output-properties-glue-items-properties-addresses.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/glue/items/properties/addresses") |

## ns_name



`ns_name`

* is required

* Type: `string`

* cannot be null

* defined in: [update-zone output](update-zone-output-properties-glue-items-properties-ns_name.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/glue/items/properties/ns_name")

### ns_name Type

`string`

## addresses



`addresses`

* is required

* Type: `string[]`

* cannot be null

* defined in: [update-zone output](update-zone-output-properties-glue-items-properties-addresses.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/glue/items/properties/addresses")

### addresses Type

`string[]`
