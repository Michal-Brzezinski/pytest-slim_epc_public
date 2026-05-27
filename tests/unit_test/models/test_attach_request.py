"""Validation tests for AttachUERequest model."""

import pytest
from pydantic import ValidationError

from epc.models import AttachUERequest


@pytest.mark.parametrize("ue_id", [1, 50, 100])
def test_attach_request_valid_range(ue_id):
    req = AttachUERequest(ue_id=ue_id)
    assert req.ue_id == ue_id


@pytest.mark.parametrize("ue_id", [0, -1, 101, 999])
def test_attach_request_invalid_range(ue_id):
    with pytest.raises(ValidationError):
        AttachUERequest(ue_id=ue_id)


@pytest.mark.parametrize("bad_value", ["abc", None, 5.7])
def test_attach_request_invalid_types(bad_value):
    # Pydantic should reject non-integer UE identifiers during validation.
    with pytest.raises(ValidationError):
        AttachUERequest(ue_id=bad_value)