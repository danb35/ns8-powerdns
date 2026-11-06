# Untitled string in add-zone input Schema

```txt
http://schema.nethserver.org/powerdns/add-zone-input.json#/properties/denial
```

NSEC3 with RFC 9276 parameters (default), or plain NSEC

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [add-zone-input.json\*](powerdns/add-zone-input.json "open original schema") |

## denial Type

`string`

## denial Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |    |    |
| :-------- | :---------- | :- | :- |
| `"nsec3"` |             |
| `"nsec"`  |             |
