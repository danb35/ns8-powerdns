# Untitled object in update-external-secondary input Schema

```txt
http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [update-external-secondary-input.json\*](powerdns/update-external-secondary-input.json "open original schema") |

## tsig Type

`object` ([Details](update-external-secondary-input-properties-tsig.md))

# tsig Properties

| Property                  | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                      |
| :------------------------ | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [algorithm](#algorithm)   | `string`  | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-tsig-properties-algorithm.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig/properties/algorithm")   |
| [key_name](#key_name)     | `string`  | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-tsig-properties-key_name.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig/properties/key_name")     |
| [secret](#secret)         | `string`  | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-tsig-properties-secret.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig/properties/secret")         |
| [regenerate](#regenerate) | `boolean` | Optional | cannot be null | [update-external-secondary input](update-external-secondary-input-properties-tsig-properties-regenerate.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig/properties/regenerate") |

## algorithm



`algorithm`

* is optional

* Type: `string`

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-tsig-properties-algorithm.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig/properties/algorithm")

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

* defined in: [update-external-secondary input](update-external-secondary-input-properties-tsig-properties-key_name.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig/properties/key_name")

### key_name Type

`string`

## secret

Base64 secret issued by the provider; generated when empty

`secret`

* is optional

* Type: `string`

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-tsig-properties-secret.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig/properties/secret")

### secret Type

`string`

## regenerate

Replace the key with a new generated one

`regenerate`

* is optional

* Type: `boolean`

* cannot be null

* defined in: [update-external-secondary input](update-external-secondary-input-properties-tsig-properties-regenerate.md "http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig/properties/regenerate")

### regenerate Type

`boolean`
