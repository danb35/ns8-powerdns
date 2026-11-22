# Untitled string in update-external-secondary input Schema

```txt
http://schema.nethserver.org/powerdns/update-external-secondary-input.json#/properties/tsig/properties/algorithm
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                                     |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [update-external-secondary-input.json\*](powerdns/update-external-secondary-input.json "open original schema") |

## algorithm Type

`string`

## algorithm Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value           | Explanation |    |    |
| :-------------- | :---------- | :- | :- |
| `"hmac-md5"`    |             |
| `"hmac-sha1"`   |             |
| `"hmac-sha224"` |             |
| `"hmac-sha256"` |             |
| `"hmac-sha384"` |             |
| `"hmac-sha512"` |             |
