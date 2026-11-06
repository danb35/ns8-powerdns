# update-zone output Schema

```txt
http://schema.nethserver.org/powerdns/update-zone-output.json
```

Change DNSSEC settings and SOA overrides of a zone

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [update-zone-output.json](powerdns/update-zone-output.json "open original schema") |

## update-zone output Type

`object` ([update-zone output](update-zone-output.md))

# update-zone output Properties

| Property                  | Type      | Required | Nullable       | Defined by                                                                                                                                               |
| :------------------------ | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone)             | `string`  | Required | cannot be null | [update-zone output](update-zone-output-properties-zone.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/zone")             |
| [kind](#kind)             | `string`  | Required | cannot be null | [update-zone output](update-zone-output-properties-kind.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/kind")             |
| [serial](#serial)         | `integer` | Required | cannot be null | [update-zone output](update-zone-output-properties-serial.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/serial")         |
| [dnssec](#dnssec)         | `boolean` | Required | cannot be null | [update-zone output](update-zone-output-properties-dnssec.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/dnssec")         |
| [denial](#denial)         | `string`  | Optional | can be null    | [update-zone output](update-zone-output-properties-denial.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/denial")         |
| [ds_records](#ds_records) | `array`   | Required | cannot be null | [update-zone output](update-zone-output-properties-ds_records.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/ds_records") |
| [glue](#glue)             | `array`   | Optional | cannot be null | [update-zone output](update-zone-output-properties-glue.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/glue")             |

## zone



`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [update-zone output](update-zone-output-properties-zone.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/zone")

### zone Type

`string`

## kind



`kind`

* is required

* Type: `string`

* cannot be null

* defined in: [update-zone output](update-zone-output-properties-kind.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/kind")

### kind Type

`string`

## serial



`serial`

* is required

* Type: `integer`

* cannot be null

* defined in: [update-zone output](update-zone-output-properties-serial.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/serial")

### serial Type

`integer`

## dnssec



`dnssec`

* is required

* Type: `boolean`

* cannot be null

* defined in: [update-zone output](update-zone-output-properties-dnssec.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/dnssec")

### dnssec Type

`boolean`

## denial



`denial`

* is optional

* Type: `string`

* can be null

* defined in: [update-zone output](update-zone-output-properties-denial.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/denial")

### denial Type

`string`

## ds_records

SHA-256 DS records for the registrar

`ds_records`

* is required

* Type: `string[]`

* cannot be null

* defined in: [update-zone output](update-zone-output-properties-ds_records.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/ds_records")

### ds_records Type

`string[]`

## glue

NS names inside the zone: the registrar needs glue for them

`glue`

* is optional

* Type: `object[]` ([Details](update-zone-output-properties-glue-items.md))

* cannot be null

* defined in: [update-zone output](update-zone-output-properties-glue.md "http://schema.nethserver.org/powerdns/update-zone-output.json#/properties/glue")

### glue Type

`object[]` ([Details](update-zone-output-properties-glue-items.md))
