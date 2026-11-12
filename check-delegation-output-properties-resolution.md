# Untitled undefined type in check-delegation output Schema

```txt
http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/resolution
```

How a validating resolver answers the zone SOA

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                     |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [check-delegation-output.json\*](powerdns/check-delegation-output.json "open original schema") |

## resolution Type

`string`

## resolution Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value        | Explanation |    |    |
| :----------- | :---------- | :- | :- |
| `"ok"`       |             |
| `"servfail"` |             |
| `"nxdomain"` |             |
| `"error"`    |             |
| `null`       |             |
