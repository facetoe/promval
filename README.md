# promval

`promval` is a PromQL validator written in Python.

It can be used to validate PromQL expressions are written as expected.

### Examples

#### Validate that we are grouping by certain metrics in by clauses

Here we validate that we are grouping by "job" and "host":
```python
promql = """
    sum by (job) (
      rate(http_requests_total[5m])
    )
"""
validator = ByGroupValidator(expected={"job", "host"})
validator.validate(promql)
```

This fails with:
```
promval.error.ValidationError: 'line: 2:12 'by (job)' - missing required metric names {'host'}
```

#### Validate that labels containing a certain value are specified in by clause

Here we ensure that if we have a label with a particular value, it is specified in the by clause:

```python
expr = """
max by (require, not_required)(foo_metric{required=~'important', something='else'})
"""
validator = ByLabelValueValidator(label_value="important")
validator.validate(expr)
```

This fails with:
```
'line: 2:4 'by (require, not_required)' - expected label name 'required' in by clause
```

### Extending promval

It is easy to write custom validators, simply subclass `promval.validators.Validator` and implement a validating visitor. See examples in `promval.validators` for more information.
