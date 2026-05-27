import pytest
from fastapi import HTTPException
from epc.api import add_bearer, delete_bearer
from epc.models import AddBearerRequest, UEState, BearerConfig

def test_add_bearer_value_error(mock_repo):
    mock_repo.add_bearer.side_effect = ValueError("Bearer limit exceeded")
    with pytest.raises(HTTPException) as exc:
        add_bearer(ue_id=1, body=AddBearerRequest(bearer_id=5), repo=mock_repo)
    assert exc.value.status_code == 400

def test_delete_bearer_ue_value_error(mock_repo):
    mock_repo.get_ue.side_effect = ValueError("UE does not exist")
    with pytest.raises(HTTPException) as exc:
        delete_bearer(ue_id=1, bearer_id=5, repo=mock_repo)
    assert exc.value.status_code == 400

def test_delete_bearer_not_in_bearers(mock_repo):
    mock_repo.get_ue.return_value = UEState(ue_id=1, bearers={})
    with pytest.raises(HTTPException) as exc:
        delete_bearer(ue_id=1, bearer_id=5, repo=mock_repo)
    assert exc.value.status_code == 400
    assert "not found" in exc.value.detail.lower()

def test_delete_bearer_running_traffic(mock_repo, mock_tm):
    mock_repo.get_ue.return_value = UEState(
        ue_id=1, bearers={5: BearerConfig(bearer_id=5)}
    )
    mock_tm.is_running.return_value = True
    response = delete_bearer(ue_id=1, bearer_id=5, repo=mock_repo)
    assert response.status == "bearer_deleted"
    mock_tm.stop.assert_called_once_with(1, 5)

def test_delete_bearer_inner_value_error(mock_repo, mock_tm):
    mock_repo.get_ue.return_value = UEState(ue_id=1, bearers={5: BearerConfig(bearer_id=5)})
    mock_tm.is_running.return_value = False
    mock_repo.delete_bearer.side_effect = ValueError("some error")
    with pytest.raises(HTTPException) as exc:
        delete_bearer(ue_id=1, bearer_id=5, repo=mock_repo)
    assert exc.value.status_code == 400
