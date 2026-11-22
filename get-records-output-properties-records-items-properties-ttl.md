# Untitled integer in get-records output Schema

```txt
http://schema.nethserver.org/powerdns/get-records-output.json#/properties/records/items/properties/ttl
```

Seconds; 0 or absent keeps 3600

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                           |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [get-records-output.json\*](powerdns/get-records-output.json "open original schema") |

## ttl Type

`integer`

## ttl Constraints

**minimum**: the value of this number must greater than or equal to: `0`
