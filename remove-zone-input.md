# remove-zone input Schema

```txt
http://schema.nethserver.org/powerdns/remove-zone-input.json
```

Delete a zone and its keys

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [remove-zone-input.json](powerdns/remove-zone-input.json "open original schema") |

## remove-zone input Type

`object` ([remove-zone input](remove-zone-input.md))

# remove-zone input Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                                |
| :------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone) | `string` | Required | cannot be null | [remove-zone input](remove-zone-input-properties-zone.md "http://schema.nethserver.org/powerdns/remove-zone-input.json#/properties/zone") |

## zone

Zone name, like example.com

`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [remove-zone input](remove-zone-input-properties-zone.md "http://schema.nethserver.org/powerdns/remove-zone-input.json#/properties/zone")

### zone Type

`string`

### zone Constraints

**minimum length**: the minimum number of characters for this string is: `1`
