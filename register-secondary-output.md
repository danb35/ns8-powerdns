# register-secondary output Schema

```txt
http://schema.nethserver.org/powerdns/register-secondary-output.json
```

Role replica. Add a secondary and return its transfer key

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                       |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [register-secondary-output.json](powerdns/register-secondary-output.json "open original schema") |

## register-secondary output Type

`object` ([register-secondary output](register-secondary-output.md))

# register-secondary output Properties

| Property                            | Type     | Required | Nullable       | Defined by                                                                                                                                                                              |
| :---------------------------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [tsig_key](#tsig_key)               | `string` | Required | cannot be null | [register-secondary output](register-secondary-output-properties-tsig_key.md "http://schema.nethserver.org/powerdns/register-secondary-output.json#/properties/tsig_key")               |
| [tsig_secret](#tsig_secret)         | `string` | Required | cannot be null | [register-secondary output](register-secondary-output-properties-tsig_secret.md "http://schema.nethserver.org/powerdns/register-secondary-output.json#/properties/tsig_secret")         |
| [algorithm](#algorithm)             | `string` | Required | cannot be null | [register-secondary output](register-secondary-output-properties-algorithm.md "http://schema.nethserver.org/powerdns/register-secondary-output.json#/properties/algorithm")             |
| [catalog](#catalog)                 | `string` | Required | cannot be null | [register-secondary output](register-secondary-output-properties-catalog.md "http://schema.nethserver.org/powerdns/register-secondary-output.json#/properties/catalog")                 |
| [primary_address](#primary_address) | `string` | Required | cannot be null | [register-secondary output](register-secondary-output-properties-primary_address.md "http://schema.nethserver.org/powerdns/register-secondary-output.json#/properties/primary_address") |

## tsig_key



`tsig_key`

* is required

* Type: `string`

* cannot be null

* defined in: [register-secondary output](register-secondary-output-properties-tsig_key.md "http://schema.nethserver.org/powerdns/register-secondary-output.json#/properties/tsig_key")

### tsig_key Type

`string`

## tsig_secret



`tsig_secret`

* is required

* Type: `string`

* cannot be null

* defined in: [register-secondary output](register-secondary-output-properties-tsig_secret.md "http://schema.nethserver.org/powerdns/register-secondary-output.json#/properties/tsig_secret")

### tsig_secret Type

`string`

## algorithm



`algorithm`

* is required

* Type: `string`

* cannot be null

* defined in: [register-secondary output](register-secondary-output-properties-algorithm.md "http://schema.nethserver.org/powerdns/register-secondary-output.json#/properties/algorithm")

### algorithm Type

`string`

## catalog



`catalog`

* is required

* Type: `string`

* cannot be null

* defined in: [register-secondary output](register-secondary-output-properties-catalog.md "http://schema.nethserver.org/powerdns/register-secondary-output.json#/properties/catalog")

### catalog Type

`string`

## primary_address



`primary_address`

* is required

* Type: `string`

* cannot be null

* defined in: [register-secondary output](register-secondary-output-properties-primary_address.md "http://schema.nethserver.org/powerdns/register-secondary-output.json#/properties/primary_address")

### primary_address Type

`string`
