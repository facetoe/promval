import pytest

from promval.error import ValidationError
from promval.validators.by_validator import ByGroupValidator


def test_validator_valid():
    expr = """
        sum by (job) (
          rate(http_requests_total[5m])
        )
    """
    validator = ByGroupValidator(expected={"job"})
    validator.validate(expr)


def test_validator_missing_group():
    expr = """
        sum by (job) (
          rate(http_requests_total[5m])
        )
    """
    validator = ByGroupValidator(expected={"job", "thing"})
    with pytest.raises(ValidationError):
        validator.validate(expr)
