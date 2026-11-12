# Untitled string in add-external-secondary input Schema

```txt
http://schema.nethserver.org/powerdns/add-external-secondary-input.json#/properties/auth
```

TSIG key (default), or source addresses only

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                               |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [add-external-secondary-input.json\*](powerdns/add-external-secondary-input.json "open original schema") |

## auth Type

`string`

## auth Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |    |    |
| :------- | :---------- | :- | :- |
| `"tsig"` |             |
| `"ip"`   |             |
