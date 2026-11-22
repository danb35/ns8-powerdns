# delete-records input Schema

```txt
http://schema.nethserver.org/powerdns/delete-records-input.json
```

Delete RRsets or single values. Refused with managed_by_dnshelper while dnshelper manages the zone

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                             |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [delete-records-input.json](powerdns/delete-records-input.json "open original schema") |

## delete-records input Type

`object` ([delete-records input](delete-records-input.md))

# delete-records input Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                               |
| :------------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone)       | `string` | Required | cannot be null | [delete-records input](delete-records-input-properties-zone.md "http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/zone")       |
| [records](#records) | `array`  | Required | cannot be null | [delete-records input](delete-records-input-properties-records.md "http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records") |

## zone

Zone name, like example.com

`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [delete-records input](delete-records-input-properties-zone.md "http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/zone")

### zone Type

`string`

### zone Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## records



`records`

* is required

* Type: `object[]` ([Details](delete-records-input-properties-records-items.md))

* cannot be null

* defined in: [delete-records input](delete-records-input-properties-records.md "http://schema.nethserver.org/powerdns/delete-records-input.json#/properties/records")

### records Type

`object[]` ([Details](delete-records-input-properties-records-items.md))

### records Constraints

**minimum number of items**: the minimum number of items for this array is: `1`
