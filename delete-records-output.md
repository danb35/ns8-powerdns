# delete-records output Schema

```txt
http://schema.nethserver.org/powerdns/delete-records-output.json
```

Delete RRsets or single values. Refused with managed_by_dnshelper while dnshelper manages the zone

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                               |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [delete-records-output.json](powerdns/delete-records-output.json "open original schema") |

## delete-records output Type

`object` ([delete-records output](delete-records-output.md))

# delete-records output Properties

| Property            | Type    | Required | Nullable       | Defined by                                                                                                                                                  |
| :------------------ | :------ | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [records](#records) | `array` | Required | cannot be null | [delete-records output](delete-records-output-properties-records.md "http://schema.nethserver.org/powerdns/delete-records-output.json#/properties/records") |

## records



`records`

* is required

* Type: `object[]` ([Details](delete-records-output-properties-records-items.md))

* cannot be null

* defined in: [delete-records output](delete-records-output-properties-records.md "http://schema.nethserver.org/powerdns/delete-records-output.json#/properties/records")

### records Type

`object[]` ([Details](delete-records-output-properties-records-items.md))
