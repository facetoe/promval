import pytest

from promval.error import ValidationError
from promval.validators.aggregation import ByGroupValidator, AggregationLabelValueValidator


def test_group_validator_valid():
    expr = """
        sum by (job) (
          rate(http_requests_total[5m])
        )
    """
    validator = ByGroupValidator(expected={"job"})
    validator.validate(expr)


def test_group_validator_complex():
    expr = """
        sum by (group, name)
        (
            sum_over_time(
                label_replace(some_metric, "name", "$1", "othername", "(.*)")[6h:]
            )
        ) > 5
    """
    validator = ByGroupValidator(expected={"name", "group"})
    validator.validate(expr)


def test_group_validator_missing_group():
    expr = """
        sum by (job) (
          rate(http_requests_total[5m])
        )
    """
    validator = ByGroupValidator(expected={"job", "thing"})
    with pytest.raises(ValidationError):
        validator.validate(expr)


def test_label_validator_valid():
    expr = """
        max by (very, second)(foo_metric{very=~'important', something='else'})
    """
    validator = AggregationLabelValueValidator(label_value="important")
    validator.validate(expr)


def test_label_validator_missing_label():
    expr = """
        max by (ve, second)(foo_metric{very=~'important', something='else'})
    """
    validator = AggregationLabelValueValidator(label_value="important")
    with pytest.raises(ValidationError):
        validator.validate(expr)


def test_label_validator_multiple_labels():
    expr = """
        avg by (first, second)(foo_metric{very=~'important'} / foo_metric{very=~'important'}) > 8
    """
    validator = AggregationLabelValueValidator(label_value="important")
    with pytest.raises(ValidationError):
        validator.validate(expr)
