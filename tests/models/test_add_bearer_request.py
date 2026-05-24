import pytest
from epc.models import AddBearerRequest

@pytest.mark.parametrize("bearer_id", [1, 5, 9])
def test_add_bearer_valid_range(bearer_id):
    req = AddBearerRequest(bearer_id=bearer_id)
    assert req.bearer_id == bearer_id

@pytest.mark.parametrize("bearer_id", [0, 10, -3])
def test_add_bearer_invalid_range(bearer_id):
    with pytest.raises(ValueError):
        AddBearerRequest(bearer_id=bearer_id)
