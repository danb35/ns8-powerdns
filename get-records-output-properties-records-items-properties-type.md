# Untitled string in get-records output Schema

```txt
http://schema.nethserver.org/powerdns/get-records-output.json#/properties/records/items/properties/type
```



| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                           |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [get-records-output.json\*](powerdns/get-records-output.json "open original schema") |

## type Type

`string`

## type Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^[A-Za-z0-9]+$
```

[try pattern](https://regexr.com/?expression=%5E%5BA-Za-z0-9%5D%2B%24 "try regular expression with regexr.com")
