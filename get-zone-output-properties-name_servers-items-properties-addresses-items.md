# Untitled object in get-zone output Schema

```txt
http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/addresses/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-zone-output.json\*](powerdns/get-zone-output.json "open original schema") |

## items Type

`object` ([Details](get-zone-output-properties-name_servers-items-properties-addresses-items.md))

# items Properties

| Property            | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                                                  |
| :------------------ | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [address](#address) | `string`  | Required | cannot be null | [get-zone output](get-zone-output-properties-name_servers-items-properties-addresses-items-properties-address.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/addresses/items/properties/address") |
| [public](#public)   | `boolean` | Required | cannot be null | [get-zone output](get-zone-output-properties-name_servers-items-properties-addresses-items-properties-public.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/addresses/items/properties/public")   |

## address



`address`

* is required

* Type: `string`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-name_servers-items-properties-addresses-items-properties-address.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/addresses/items/properties/address")

### address Type

`string`

## public

False for a private or local address, which cannot be glue

`public`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-name_servers-items-properties-addresses-items-properties-public.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers/items/properties/addresses/items/properties/public")

### public Type

`boolean`
