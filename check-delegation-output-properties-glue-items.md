# Untitled object in check-delegation output Schema

```txt
http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                                     |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [check-delegation-output.json\*](powerdns/check-delegation-output.json "open original schema") |

## items Type

`object` ([Details](check-delegation-output-properties-glue-items.md))

# items Properties

| Property                | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                        |
| :---------------------- | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ns_name](#ns_name)     | `string`  | Required | cannot be null | [check-delegation output](check-delegation-output-properties-glue-items-properties-ns_name.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items/properties/ns_name")     |
| [expected](#expected)   | `array`   | Required | cannot be null | [check-delegation output](check-delegation-output-properties-glue-items-properties-expected.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items/properties/expected")   |
| [published](#published) | `array`   | Required | cannot be null | [check-delegation output](check-delegation-output-properties-glue-items-properties-published.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items/properties/published") |
| [ok](#ok)               | `boolean` | Required | cannot be null | [check-delegation output](check-delegation-output-properties-glue-items-properties-ok.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items/properties/ok")               |

## ns_name



`ns_name`

* is required

* Type: `string`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-glue-items-properties-ns_name.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items/properties/ns_name")

### ns_name Type

`string`

## expected



`expected`

* is required

* Type: `string[]`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-glue-items-properties-expected.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items/properties/expected")

### expected Type

`string[]`

## published



`published`

* is required

* Type: `string[]`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-glue-items-properties-published.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items/properties/published")

### published Type

`string[]`

## ok



`ok`

* is required

* Type: `boolean`

* cannot be null

* defined in: [check-delegation output](check-delegation-output-properties-glue-items-properties-ok.md "http://schema.nethserver.org/powerdns/check-delegation-output.json#/properties/glue/items/properties/ok")

### ok Type

`boolean`
