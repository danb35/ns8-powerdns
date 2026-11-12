# list-secondaries output Schema

```txt
http://schema.nethserver.org/powerdns/list-secondaries-output.json
```

Registered secondaries, with replication lag, and secondaries outside the cluster

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [list-secondaries-output.json](powerdns/list-secondaries-output.json "open original schema") |

## list-secondaries output Type

`object` ([list-secondaries output](list-secondaries-output.md))

# list-secondaries output Properties

| Property                    | Type    | Required | Nullable       | Defined by                                                                                                                                                                |
| :-------------------------- | :------ | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [secondaries](#secondaries) | `array` | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-secondaries.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries") |
| [external](#external)       | `array` | Required | cannot be null | [list-secondaries output](list-secondaries-output-properties-external.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external")       |

## secondaries



`secondaries`

* is required

* Type: `object[]` ([Details](list-secondaries-output-properties-secondaries-items.md))

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-secondaries.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/secondaries")

### secondaries Type

`object[]` ([Details](list-secondaries-output-properties-secondaries-items.md))

## external



`external`

* is required

* Type: `object[]` ([Details](list-secondaries-output-properties-external-items.md))

* cannot be null

* defined in: [list-secondaries output](list-secondaries-output-properties-external.md "http://schema.nethserver.org/powerdns/list-secondaries-output.json#/properties/external")

### external Type

`object[]` ([Details](list-secondaries-output-properties-external-items.md))
