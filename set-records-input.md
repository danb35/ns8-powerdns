# set-records input Schema

```txt
http://schema.nethserver.org/powerdns/set-records-input.json
```

Each name and type in the input becomes exactly the values given. Refused with managed_by_dnshelper while dnshelper manages the zone

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [set-records-input.json](powerdns/set-records-input.json "open original schema") |

## set-records input Type

`object` ([set-records input](set-records-input.md))

# set-records input Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                      |
| :------------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone)       | `string` | Required | cannot be null | [set-records input](set-records-input-properties-zone.md "http://schema.nethserver.org/powerdns/set-records-input.json#/properties/zone")       |
| [records](#records) | `array`  | Required | cannot be null | [set-records input](set-records-input-properties-records.md "http://schema.nethserver.org/powerdns/set-records-input.json#/properties/records") |

## zone

Zone name, like example.com

`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [set-records input](set-records-input-properties-zone.md "http://schema.nethserver.org/powerdns/set-records-input.json#/properties/zone")

### zone Type

`string`

### zone Constraints

**minimum length**: the minimum number of characters for this string is: `1`

## records



`records`

* is required

* Type: `object[]` ([Details](set-records-input-properties-records-items.md))

* cannot be null

* defined in: [set-records input](set-records-input-properties-records.md "http://schema.nethserver.org/powerdns/set-records-input.json#/properties/records")

### records Type

`object[]` ([Details](set-records-input-properties-records-items.md))

### records Constraints

**minimum number of items**: the minimum number of items for this array is: `1`
