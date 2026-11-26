# remove-secondary input Schema

```txt
http://schema.nethserver.org/powerdns/remove-secondary-input.json
```

Remove a stale secondary entry and revoke its key

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                 |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [remove-secondary-input.json](powerdns/remove-secondary-input.json "open original schema") |

## remove-secondary input Type

`object` ([remove-secondary input](remove-secondary-input.md))

# remove-secondary input Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                                         |
| :---------------------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [module_id](#module_id) | `string` | Required | cannot be null | [remove-secondary input](remove-secondary-input-properties-module_id.md "http://schema.nethserver.org/powerdns/remove-secondary-input.json#/properties/module_id") |

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [remove-secondary input](remove-secondary-input-properties-module_id.md "http://schema.nethserver.org/powerdns/remove-secondary-input.json#/properties/module_id")

### module_id Type

`string`

### module_id Constraints

**minimum length**: the minimum number of characters for this string is: `1`
