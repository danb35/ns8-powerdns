# get-records output Schema

```txt
http://schema.nethserver.org/powerdns/get-records-output.json
```

Records of a zone, and whether this module may edit them

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [get-records-output.json](powerdns/get-records-output.json "open original schema") |

## get-records output Type

`object` ([get-records output](get-records-output.md))

# get-records output Properties

| Property                                      | Type      | Required | Nullable       | Defined by                                                                                                                                                                   |
| :-------------------------------------------- | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone)                                 | `string`  | Required | cannot be null | [get-records output](get-records-output-properties-zone.md "http://schema.nethserver.org/powerdns/get-records-output.json#/properties/zone")                                 |
| [records](#records)                           | `array`   | Required | cannot be null | [get-records output](get-records-output-properties-records.md "http://schema.nethserver.org/powerdns/get-records-output.json#/properties/records")                           |
| [managed_by_dnshelper](#managed_by_dnshelper) | `boolean` | Required | cannot be null | [get-records output](get-records-output-properties-managed_by_dnshelper.md "http://schema.nethserver.org/powerdns/get-records-output.json#/properties/managed_by_dnshelper") |
| [dnshelper_module_id](#dnshelper_module_id)   | `string`  | Required | cannot be null | [get-records output](get-records-output-properties-dnshelper_module_id.md "http://schema.nethserver.org/powerdns/get-records-output.json#/properties/dnshelper_module_id")   |
| [editable](#editable)                         | `boolean` | Required | cannot be null | [get-records output](get-records-output-properties-editable.md "http://schema.nethserver.org/powerdns/get-records-output.json#/properties/editable")                         |

## zone



`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [get-records output](get-records-output-properties-zone.md "http://schema.nethserver.org/powerdns/get-records-output.json#/properties/zone")

### zone Type

`string`

## records



`records`

* is required

* Type: `object[]` ([Details](get-records-output-properties-records-items.md))

* cannot be null

* defined in: [get-records output](get-records-output-properties-records.md "http://schema.nethserver.org/powerdns/get-records-output.json#/properties/records")

### records Type

`object[]` ([Details](get-records-output-properties-records-items.md))

## managed_by_dnshelper



`managed_by_dnshelper`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-records output](get-records-output-properties-managed_by_dnshelper.md "http://schema.nethserver.org/powerdns/get-records-output.json#/properties/managed_by_dnshelper")

### managed_by_dnshelper Type

`boolean`

## dnshelper_module_id



`dnshelper_module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [get-records output](get-records-output-properties-dnshelper_module_id.md "http://schema.nethserver.org/powerdns/get-records-output.json#/properties/dnshelper_module_id")

### dnshelper_module_id Type

`string`

## editable



`editable`

* is required

* Type: `boolean`

* cannot be null

* defined in: [get-records output](get-records-output-properties-editable.md "http://schema.nethserver.org/powerdns/get-records-output.json#/properties/editable")

### editable Type

`boolean`
