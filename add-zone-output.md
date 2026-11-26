# add-zone output Schema

```txt
http://schema.nethserver.org/powerdns/add-zone-output.json
```

Create a zone on the primary

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [add-zone-output.json](powerdns/add-zone-output.json "open original schema") |

## add-zone output Type

`object` ([add-zone output](add-zone-output.md))

# add-zone output Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                          |
| :------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| [zone](#zone) | `string` | Required | cannot be null | [add-zone output](add-zone-output-properties-zone.md "http://schema.nethserver.org/powerdns/add-zone-output.json#/properties/zone") |
| [glue](#glue) | `array`  | Required | cannot be null | [add-zone output](add-zone-output-properties-glue.md "http://schema.nethserver.org/powerdns/add-zone-output.json#/properties/glue") |

## zone



`zone`

* is required

* Type: `string`

* cannot be null

* defined in: [add-zone output](add-zone-output-properties-zone.md "http://schema.nethserver.org/powerdns/add-zone-output.json#/properties/zone")

### zone Type

`string`

## glue

NS names inside the zone: the registrar needs glue for them

`glue`

* is required

* Type: `object[]` ([Details](add-zone-output-properties-glue-items.md))

* cannot be null

* defined in: [add-zone output](add-zone-output-properties-glue.md "http://schema.nethserver.org/powerdns/add-zone-output.json#/properties/glue")

### glue Type

`object[]` ([Details](add-zone-output-properties-glue-items.md))
