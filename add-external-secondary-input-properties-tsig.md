# Untitled object in add-external-secondary input Schema

```txt
http://schema.nethserver.org/powerdns/add-external-secondary-input.json#/properties/tsig
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                               |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [add-external-secondary-input.json\*](powerdns/add-external-secondary-input.json "open original schema") |

## tsig Type

`object` ([Details](add-external-secondary-input-properties-tsig.md))

# tsig Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                           |
| :---------------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [algorithm](#algorithm) | `string` | Optional | cannot be null | [add-external-secondary input](add-external-secondary-input-properties-tsig-properties-algorithm.md "http://schema.nethserver.org/powerdns/add-external-secondary-input.json#/properties/tsig/properties/algorithm") |
| [key_name](#key_name)   | `string` | Optional | cannot be null | [add-external-secondary input](add-external-secondary-input-properties-tsig-properties-key_name.md "http://schema.nethserver.org/powerdns/add-external-secondary-input.json#/properties/tsig/properties/key_name")   |
| [secret](#secret)       | `string` | Optional | cannot be null | [add-external-secondary input](add-external-secondary-input-properties-tsig-properties-secret.md "http://schema.nethserver.org/powerdns/add-external-secondary-input.json#/properties/tsig/properties/secret")       |

## algorithm



`algorithm`

* is optional

* Type: `string`

* cannot be null

* defined in: [add-external-secondary input](add-external-secondary-input-properties-tsig-properties-algorithm.md "http://schema.nethserver.org/powerdns/add-external-secondary-input.json#/properties/tsig/properties/algorithm")

### algorithm Type

`string`

### algorithm Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value           | Explanation |    |    |
| :-------------- | :---------- | :- | :- |
| `"hmac-md5"`    |             |
| `"hmac-sha1"`   |             |
| `"hmac-sha224"` |             |
| `"hmac-sha256"` |             |
| `"hmac-sha384"` |             |
| `"hmac-sha512"` |             |

## key_name

Defaults to powerdns-<id>

`key_name`

* is optional

* Type: `string`

* cannot be null

* defined in: [add-external-secondary input](add-external-secondary-input-properties-tsig-properties-key_name.md "http://schema.nethserver.org/powerdns/add-external-secondary-input.json#/properties/tsig/properties/key_name")

### key_name Type

`string`

## secret

Base64 secret issued by the provider; generated when empty

`secret`

* is optional

* Type: `string`

* cannot be null

* defined in: [add-external-secondary input](add-external-secondary-input-properties-tsig-properties-secret.md "http://schema.nethserver.org/powerdns/add-external-secondary-input.json#/properties/tsig/properties/secret")

### secret Type

`string`
