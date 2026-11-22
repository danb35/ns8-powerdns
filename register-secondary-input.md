# register-secondary input Schema

```txt
http://schema.nethserver.org/powerdns/register-secondary-input.json
```

Role replica. Add a secondary and return its transfer key

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [register-secondary-input.json](powerdns/register-secondary-input.json "open original schema") |

## register-secondary input Type

`object` ([register-secondary input](register-secondary-input.md))

# register-secondary input Properties

| Property                | Type      | Required | Nullable       | Defined by                                                                                                                                                               |
| :---------------------- | :-------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [module_id](#module_id) | `string`  | Required | cannot be null | [register-secondary input](register-secondary-input-properties-module_id.md "http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/module_id") |
| [address](#address)     | `string`  | Required | cannot be null | [register-secondary input](register-secondary-input-properties-address.md "http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/address")     |
| [ns_name](#ns_name)     | `string`  | Optional | cannot be null | [register-secondary input](register-secondary-input-properties-ns_name.md "http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/ns_name")     |
| [advertise](#advertise) | `boolean` | Optional | cannot be null | [register-secondary input](register-secondary-input-properties-advertise.md "http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/advertise") |
| [addresses](#addresses) | `array`   | Optional | cannot be null | [register-secondary input](register-secondary-input-properties-addresses.md "http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/addresses") |

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [register-secondary input](register-secondary-input-properties-module_id.md "http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/module_id")

### module_id Type

`string`

### module_id Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## address

The secondary's VPN address

`address`

* is required

* Type: `string`

* cannot be null

* defined in: [register-secondary input](register-secondary-input-properties-address.md "http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/address")

### address Type

`string`

### address Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## ns_name



`ns_name`

* is optional

* Type: `string`

* cannot be null

* defined in: [register-secondary input](register-secondary-input-properties-ns_name.md "http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/ns_name")

### ns_name Type

`string`

## advertise



`advertise`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [register-secondary input](register-secondary-input-properties-advertise.md "http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/advertise")

### advertise Type

`boolean`

## addresses

Its public addresses, shown as glue

`addresses`

* is optional

* Type: `string[]`

* cannot be null

* defined in: [register-secondary input](register-secondary-input-properties-addresses.md "http://schema.nethserver.org/powerdns/register-secondary-input.json#/properties/addresses")

### addresses Type

`string[]`
