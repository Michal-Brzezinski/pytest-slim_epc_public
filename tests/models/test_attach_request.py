import pytest
from epc.models import AttachUERequest

@pytest.mark.parametrize("ue_id", [1, 50, 100])
def test_attach_request_valid_range(ue_id):
    req = AttachUERequest(ue_id=ue_id)
    assert req.ue_id == ue_id

@pytest.mark.parametrize("ue_id", [0, -1, 101, 999])
def test_attach_request_invalid_range(ue_id):
    with pytest.raises(ValueError):
        AttachUERequest(ue_id=ue_id)
