# add-external-secondary output Schema

```txt
http://schema.nethserver.org/powerdns/add-external-secondary-output.json
```

The new peer, and its TSIG key when it uses one

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                               |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [add-external-secondary-output.json](powerdns/add-external-secondary-output.json "open original schema") |

## add-external-secondary output Type

`object` ([add-external-secondary output](add-external-secondary-output.md))

# add-external-secondary output Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                                                              |
| :---------------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [secondary](#secondary) | `object` | Required | cannot be null | [add-external-secondary output](add-external-secondary-output-properties-secondary.md "http://schema.nethserver.org/powerdns/add-external-secondary-output.json#/properties/secondary") |
| [key](#key)             | `object` | Optional | cannot be null | [add-external-secondary output](add-external-secondary-output-properties-key.md "http://schema.nethserver.org/powerdns/add-external-secondary-output.json#/properties/key")             |

## secondary



`secondary`

* is required

* Type: `object` ([Details](add-external-secondary-output-properties-secondary.md))

* cannot be null

* defined in: [add-external-secondary output](add-external-secondary-output-properties-secondary.md "http://schema.nethserver.org/powerdns/add-external-secondary-output.json#/properties/secondary")

### secondary Type

`object` ([Details](add-external-secondary-output-properties-secondary.md))

## key



`key`

* is optional

* Type: `object` ([Details](add-external-secondary-output-properties-key.md))

* cannot be null

* defined in: [add-external-secondary output](add-external-secondary-output-properties-key.md "http://schema.nethserver.org/powerdns/add-external-secondary-output.json#/properties/key")

### key Type

`object` ([Details](add-external-secondary-output-properties-key.md))
