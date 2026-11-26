# update-zone input Schema

```txt
http://schema.nethserver.org/powerdns/update-zone-input.json
```

Change DNSSEC settings and SOA overrides of a zone

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [update-zone-input.json](powerdns/update-zone-input.json "open original schema") |

## update-zone input Type

`object` ([update-zone input](update-zone-input.md))

# update-zone input Properties

| Property                    | Type      | Required | Nullable       | Defined by                                                                                                                                              |
| :-------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [zone](#zone)               | `string`  | Required | cannot be null | [update-zone input](update-zone-input-properties-zone.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/zone")               |
| [dnssec](#dnssec)           | `boolean` | Optional | cannot be null | [update-zone input](update-zone-input-properties-dnssec.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/dnssec")           |
| [denial](#denial)           | `string`  | Optional | cannot be null | [update-zone input](update-zone-input-properties-denial.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/denial")           |
| [soa_refresh](#soa_refresh) | `integer` | Optional | cannot be null | [update-zone input](update-zone-input-properties-soa_refresh.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/soa_refresh") |
| [soa_retry](#soa_retry)     | `integer` | Optional | cannot be null | [update-zone input](update-zone-input-properties-soa_retry.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/soa_retry")     |
| [soa_expire](#soa_expire)   | `integer` | Optional | cannot be null | [update-zone input](update-zone-input-properties-soa_expire.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/soa_expire")   |
| [soa_minimum](#soa_minimum) | `integer` | Optional | cannot be null | [update-zone input](update-zone-input-properties-soa_minimum.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/soa_minimum") |

## zone

Zone name, like example.com

`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [update-zone input](update-zone-input-properties-zone.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/zone")

### zone Type

`string`

### zone Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## dnssec



`dnssec`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [update-zone input](update-zone-input-properties-dnssec.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/dnssec")

### dnssec Type

`boolean`

## denial

NSEC3 with RFC 9276 parameters (default), or plain NSEC

`denial`

* is optional

* Type: `string`

* cannot be null

* defined in: [update-zone input](update-zone-input-properties-denial.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/denial")

### denial Type

`string`

### denial Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |    |    |
| :-------- | :---------- | :- | :- |
| `"nsec3"` |             |
| `"nsec"`  |             |

## soa_refresh



`soa_refresh`

* is optional

* Type: `integer`

* cannot be null

* defined in: [update-zone input](update-zone-input-properties-soa_refresh.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/soa_refresh")

### soa_refresh Type

`integer`

### soa_refresh Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## soa_retry



`soa_retry`

* is optional

* Type: `integer`

* cannot be null

* defined in: [update-zone input](update-zone-input-properties-soa_retry.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/soa_retry")

### soa_retry Type

`integer`

### soa_retry Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## soa_expire



`soa_expire`

* is optional

* Type: `integer`

* cannot be null

* defined in: [update-zone input](update-zone-input-properties-soa_expire.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/soa_expire")

### soa_expire Type

`integer`

### soa_expire Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## soa_minimum



`soa_minimum`

* is optional

* Type: `integer`

* cannot be null

* defined in: [update-zone input](update-zone-input-properties-soa_minimum.md "http://schema.nethserver.org/powerdns/update-zone-input.json#/properties/soa_minimum")

### soa_minimum Type

`integer`

### soa_minimum Constraints

**minimum**: the value of this number must greater than or equal to: `1`
