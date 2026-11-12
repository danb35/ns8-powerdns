# update-external-secondary output Schema

```txt
http://schema.nethserver.org/powerdns/update-external-secondary-output.json
```

The peer, and its TSIG key when a new one was made

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [update-external-secondary-output.json](powerdns/update-external-secondary-output.json "open original schema") |

## update-external-secondary output Type

`object` ([update-external-secondary output](update-external-secondary-output.md))

# update-external-secondary output Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                                                                       |
| :---------------------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [secondary](#secondary) | `object` | Required | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-secondary.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary") |
| [key](#key)             | `object` | Optional | cannot be null | [update-external-secondary output](update-external-secondary-output-properties-key.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/key")             |

## secondary



`secondary`

* is required

* Type: `object` ([Details](update-external-secondary-output-properties-secondary.md))

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-secondary.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/secondary")

### secondary Type

`object` ([Details](update-external-secondary-output-properties-secondary.md))

## key



`key`

* is optional

* Type: `object` ([Details](update-external-secondary-output-properties-key.md))

* cannot be null

* defined in: [update-external-secondary output](update-external-secondary-output-properties-key.md "http://schema.nethserver.org/powerdns/update-external-secondary-output.json#/properties/key")

### key Type

`object` ([Details](update-external-secondary-output-properties-key.md))
