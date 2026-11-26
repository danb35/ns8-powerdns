# get-zone output Schema

```txt
http://schema.nethserver.org/powerdns/get-zone-output.json
```

One zone, with what the registrar needs on a primary

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [get-zone-output.json](powerdns/get-zone-output.json "open original schema") |

## get-zone output Type

`object` ([get-zone output](get-zone-output.md))

# get-zone output Properties

| Property                          | Type      | Required | Nullable       | Defined by                                                                                                                                              |
| :-------------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [zone](#zone)                     | `string`  | Required | cannot be null | [get-zone output](get-zone-output-properties-zone.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/zone")                     |
| [kind](#kind)                     | `string`  | Required | cannot be null | [get-zone output](get-zone-output-properties-kind.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/kind")                     |
| [serial](#serial)                 | `integer` | Required | cannot be null | [get-zone output](get-zone-output-properties-serial.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/serial")                 |
| [dnssec](#dnssec)                 | `boolean` | Required | cannot be null | [get-zone output](get-zone-output-properties-dnssec.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/dnssec")                 |
| [denial](#denial)                 | `string`  | Optional | can be null    | [get-zone output](get-zone-output-properties-denial.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/denial")                 |
| [ds_records](#ds_records)         | `array`   | Required | cannot be null | [get-zone output](get-zone-output-properties-ds_records.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/ds_records")         |
| [dnskey_records](#dnskey_records) | `array`   | Required | cannot be null | [get-zone output](get-zone-output-properties-dnskey_records.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/dnskey_records") |
| [name_servers](#name_servers)     | `array`   | Optional | cannot be null | [get-zone output](get-zone-output-properties-name_servers.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers")     |

## zone



`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-zone.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/zone")

### zone Type

`string`

## kind



`kind`

* is required

* Type: `string`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-kind.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/kind")

### kind Type

`string`

## serial



`serial`

* is required

* Type: `integer`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-serial.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/serial")

### serial Type

`integer`

## dnssec



`dnssec`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-dnssec.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/dnssec")

### dnssec Type

`boolean`

## denial



`denial`

* is optional

* Type: `string`

* can be null

* defined in: [get-zone output](get-zone-output-properties-denial.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/denial")

### denial Type

`string`

## ds_records

SHA-256 DS records for the registrar

`ds_records`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-ds_records.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/ds_records")

### ds_records Type

`string[]`

## dnskey_records

The zone's published DNSKEY records, for registries that ask for the key instead of a DS

`dnskey_records`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-dnskey_records.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/dnskey_records")

### dnskey_records Type

`string[]`

## name_servers

On a primary: the NS names to give the registrar, whether each needs glue, and its known addresses

`name_servers`

* is optional

* Type: `object[]` ([Details](get-zone-output-properties-name_servers-items.md))

* cannot be null

* defined in: [get-zone output](get-zone-output-properties-name_servers.md "http://schema.nethserver.org/powerdns/get-zone-output.json#/properties/name_servers")

### name_servers Type

`object[]` ([Details](get-zone-output-properties-name_servers-items.md))
