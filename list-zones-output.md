# list-zones output Schema

```txt
http://schema.nethserver.org/powerdns/list-zones-output.json
```

Zones served by this instance

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [list-zones-output.json](powerdns/list-zones-output.json "open original schema") |

## list-zones output Type

`object` ([list-zones output](list-zones-output.md))

# list-zones output Properties

| Property        | Type    | Required | Nullable       | Defined by                                                                                                                                  |
| :-------------- | :------ | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| [zones](#zones) | `array` | Required | cannot be null | [list-zones output](list-zones-output-properties-zones.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones") |

## zones



`zones`

* is required

* Type: `object[]` ([Details](list-zones-output-properties-zones-items.md))

* cannot be null

* defined in: [list-zones output](list-zones-output-properties-zones.md "http://schema.nethserver.org/powerdns/list-zones-output.json#/properties/zones")

### zones Type

`object[]` ([Details](list-zones-output-properties-zones-items.md))
