# promval

`promval` is a PromQL validator written in Python.

It can be used to validate PromQL expressions are written as expected.

### Example

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

### Extending promval

It is easy to write custom validators, simply subclass `promval.validators.Validator` and implement a validating visitor. See examples in `promval.validators` for more information.
