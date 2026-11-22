# set-records output Schema

```txt
http://schema.nethserver.org/powerdns/set-records-output.json
```

Each name and type in the input becomes exactly the values given. Refused with managed_by_dnshelper while dnshelper manages the zone

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [set-records-output.json](powerdns/set-records-output.json "open original schema") |

## set-records output Type

`object` ([set-records output](set-records-output.md))

# set-records output Properties

| Property            | Type    | Required | Nullable       | Defined by                                                                                                                                         |
| :------------------ | :------ | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| [records](#records) | `array` | Required | cannot be null | [set-records output](set-records-output-properties-records.md "http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records") |

## records



`records`

* is required

* Type: `object[]` ([Details](set-records-output-properties-records-items.md))

* cannot be null

* defined in: [set-records output](set-records-output-properties-records.md "http://schema.nethserver.org/powerdns/set-records-output.json#/properties/records")

### records Type

`object[]` ([Details](set-records-output-properties-records-items.md))
