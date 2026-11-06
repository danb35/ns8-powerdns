# unregister-secondary input Schema

```txt
http://schema.nethserver.org/powerdns/unregister-secondary-input.json
```

Role replica. Forget a secondary and revoke its key

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                         |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [unregister-secondary-input.json](powerdns/unregister-secondary-input.json "open original schema") |

## unregister-secondary input Type

`object` ([unregister-secondary input](unregister-secondary-input.md))

# unregister-secondary input Properties

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                                                     |
| :---------------------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [module_id](#module_id) | `string` | Required | cannot be null | [unregister-secondary input](unregister-secondary-input-properties-module_id.md "http://schema.nethserver.org/powerdns/unregister-secondary-input.json#/properties/module_id") |

## module_id



`module_id`

* is required

* Type: `string`

* cannot be null

* defined in: [unregister-secondary input](unregister-secondary-input-properties-module_id.md "http://schema.nethserver.org/powerdns/unregister-secondary-input.json#/properties/module_id")

### module_id Type

`string`

### module_id Constraints

**minimum length**: the minimum number of characters for this string is: `1`
