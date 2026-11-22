# get-external-secondary-key output Schema

```txt
http://schema.nethserver.org/powerdns/get-external-secondary-key-output.json
```

The TSIG key to give the provider

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                                       |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [get-external-secondary-key-output.json](powerdns/get-external-secondary-key-output.json "open original schema") |

## get-external-secondary-key output Type

`object` ([get-external-secondary-key output](get-external-secondary-key-output.md))

# get-external-secondary-key output Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                                                                          |
| :---------------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [key_name](#key_name)   | `string` | Required | cannot be null | [get-external-secondary-key output](get-external-secondary-key-output-properties-key_name.md "http://schema.nethserver.org/powerdns/get-external-secondary-key-output.json#/properties/key_name")   |
| [algorithm](#algorithm) | `string` | Required | cannot be null | [get-external-secondary-key output](get-external-secondary-key-output-properties-algorithm.md "http://schema.nethserver.org/powerdns/get-external-secondary-key-output.json#/properties/algorithm") |
| [secret](#secret)       | `string` | Required | cannot be null | [get-external-secondary-key output](get-external-secondary-key-output-properties-secret.md "http://schema.nethserver.org/powerdns/get-external-secondary-key-output.json#/properties/secret")       |

## key_name



`key_name`

* is required

* Type: `string`

* cannot be null

* defined in: [get-external-secondary-key output](get-external-secondary-key-output-properties-key_name.md "http://schema.nethserver.org/powerdns/get-external-secondary-key-output.json#/properties/key_name")

### key_name Type

`string`

## algorithm



`algorithm`

* is required

* Type: `string`

* cannot be null

* defined in: [get-external-secondary-key output](get-external-secondary-key-output-properties-algorithm.md "http://schema.nethserver.org/powerdns/get-external-secondary-key-output.json#/properties/algorithm")

### algorithm Type

`string`

## secret



`secret`

* is required

* Type: `string`

* cannot be null

* defined in: [get-external-secondary-key output](get-external-secondary-key-output-properties-secret.md "http://schema.nethserver.org/powerdns/get-external-secondary-key-output.json#/properties/secret")

### secret Type

`string`
