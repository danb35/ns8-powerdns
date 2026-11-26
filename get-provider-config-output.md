# get-provider-config output Schema

```txt
http://schema.nethserver.org/powerdns/get-provider-config-output.json
```

Role dnsprovider. What dnshelper needs to adopt this server's zones

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                         |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [get-provider-config-output.json](powerdns/get-provider-config-output.json "open original schema") |

## get-provider-config output Type

`object` ([get-provider-config output](get-provider-config-output.md))

# get-provider-config output Properties

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                                                                   |
| :-------------------- | :------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [provider](#provider) | `string` | Required | cannot be null | [get-provider-config output](get-provider-config-output-properties-provider.md "http://schema.nethserver.org/powerdns/get-provider-config-output.json#/properties/provider") |
| [fields](#fields)     | `object` | Required | cannot be null | [get-provider-config output](get-provider-config-output-properties-fields.md "http://schema.nethserver.org/powerdns/get-provider-config-output.json#/properties/fields")     |
| [zones](#zones)       | `array`  | Required | cannot be null | [get-provider-config output](get-provider-config-output-properties-zones.md "http://schema.nethserver.org/powerdns/get-provider-config-output.json#/properties/zones")       |

## provider



`provider`

* is required

* Type: `string`

* cannot be null

* defined in: [get-provider-config output](get-provider-config-output-properties-provider.md "http://schema.nethserver.org/powerdns/get-provider-config-output.json#/properties/provider")

### provider Type

`string`

### provider Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value        | Explanation |    |    |
| :----------- | :---------- | :- | :- |
| `"powerdns"` |             |

## fields



`fields`

* is required

* Type: `object` ([Details](get-provider-config-output-properties-fields.md))

* cannot be null

* defined in: [get-provider-config output](get-provider-config-output-properties-fields.md "http://schema.nethserver.org/powerdns/get-provider-config-output.json#/properties/fields")

### fields Type

`object` ([Details](get-provider-config-output-properties-fields.md))

## zones



`zones`

* is required

* Type: `string[]`

* cannot be null

* defined in: [get-provider-config output](get-provider-config-output-properties-zones.md "http://schema.nethserver.org/powerdns/get-provider-config-output.json#/properties/zones")

### zones Type

`string[]`
