# get-records input Schema

```txt
http://schema.nethserver.org/powerdns/get-records-input.json
```

Records of a zone, and whether this module may edit them

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [get-records-input.json](powerdns/get-records-input.json "open original schema") |

## get-records input Type

`object` ([get-records input](get-records-input.md))

# get-records input Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                                |
| :------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone) | `string` | Required | cannot be null | [get-records input](get-records-input-properties-zone.md "http://schema.nethserver.org/powerdns/get-records-input.json#/properties/zone") |

## zone

Zone name, like example.com

`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [get-records input](get-records-input-properties-zone.md "http://schema.nethserver.org/powerdns/get-records-input.json#/properties/zone")

### zone Type

`string`

### zone Constraints

**minimum length**: the minimum number of characters for this string is: `1`
