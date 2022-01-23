import pytest

from promval.error import ValidationError
from promval.validators.by_validator import ByGroupValidator, ByLabelValueValidator


def test_group_validator_valid():
    expr = """
        sum by (job) (
          rate(http_requests_total[5m])
        )
    """
    validator = ByGroupValidator(expected={"job"})
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
    validator = ByLabelValueValidator(label_value="important")
    validator.validate(expr)


def test_label_validator_missing_label():
    expr = """
        max by (ve, second)(foo_metric{very=~'important', something='else'})
    """
    validator = ByLabelValueValidator(label_value="important")
    with pytest.raises(ValidationError):
        validator.validate(expr)