# check-delegation input Schema

```txt
http://schema.nethserver.org/powerdns/check-delegation-input.json
```

Compare what the parent zone publishes for a zone with what the zone needs at the registrar. Informational

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                 |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [check-delegation-input.json](powerdns/check-delegation-input.json "open original schema") |

## check-delegation input Type

`object` ([check-delegation input](check-delegation-input.md))

## check-delegation input Examples

```json
{
  "zone": "example.com"
}
```

# check-delegation input Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                                               |
| :------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone) | `string` | Required | cannot be null | [check-delegation input](check-delegation-input-properties-zone.md "http://schema.nethserver.org/powerdns/check-delegation-input.json#/properties/zone") |

## zone

Zone name, like example.com

`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [check-delegation input](check-delegation-input-properties-zone.md "http://schema.nethserver.org/powerdns/check-delegation-input.json#/properties/zone")

### zone Type

`string`

### zone Constraints

**minimum length**: the minimum number of characters for this string is: `1`
