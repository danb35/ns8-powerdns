# get-zone input Schema

```txt
http://schema.nethserver.org/powerdns/get-zone-input.json
```

One zone, with DS records on a primary

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                 |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [get-zone-input.json](powerdns/get-zone-input.json "open original schema") |

## get-zone input Type

`object` ([get-zone input](get-zone-input.md))

# get-zone input Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                       |
| :------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone) | `string` | Required | cannot be null | [get-zone input](get-zone-input-properties-zone.md "http://schema.nethserver.org/powerdns/get-zone-input.json#/properties/zone") |

## zone

Zone name, like example.com

`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [get-zone input](get-zone-input-properties-zone.md "http://schema.nethserver.org/powerdns/get-zone-input.json#/properties/zone")

### zone Type

`string`

### zone Constraints

**minimum length**: the minimum number of characters for this string is: `1`
