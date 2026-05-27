"""Validation tests for AddBearerRequest model."""

import pytest
from pydantic import ValidationError

from epc.models import AddBearerRequest


@pytest.mark.parametrize("bearer_id", [1, 5, 9])
def test_add_bearer_valid_range(bearer_id):
    req = AddBearerRequest(bearer_id=bearer_id)

    assert req.bearer_id == bearer_id


@pytest.mark.parametrize("bearer_id", [0, 10, -3])
def test_add_bearer_invalid_range(bearer_id):
    with pytest.raises(ValidationError):
        AddBearerRequest(bearer_id=bearer_id)


def test_add_bearer_string_number_is_coerced():
    # Pydantic automatically coerces numeric strings to integers.
    req = AddBearerRequest(bearer_id="5")

    assert req.bearer_id == 5


def test_add_bearer_float_rejected():
    with pytest.raises(ValidationError):
        AddBearerRequest(bearer_id=1.5)