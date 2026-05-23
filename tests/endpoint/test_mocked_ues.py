import pytest
from fastapi import HTTPException
from epc.api import attach_ue, get_ue, detach_ue
from epc.models import AttachUERequest

def test_attach_ue_value_error(mock_repo):
    """Zwracanie wyjątku przez repo rzuca HTTPException(400)."""
    mock_repo.attach_ue.side_effect = ValueError("Already exists")
    with pytest.raises(HTTPException) as exc:
        attach_ue(body=AttachUERequest(ue_id=1), repo=mock_repo)
    assert exc.value.status_code == 400
    assert "already exists" in exc.value.detail.lower()

def test_get_ue_value_error(mock_repo):
    """Próba pobrania nieistniejącego UE rzuca HTTPException(400)."""
    mock_repo.get_ue.side_effect = ValueError("UE not found")
    with pytest.raises(HTTPException) as exc:
        get_ue(ue_id=99, repo=mock_repo)
    assert exc.value.status_code == 400

def test_detach_ue_value_error(mock_repo):
    """Błąd logiki przy usuwaniu terminala rzuca HTTPException(400)."""
    mock_repo.detach_ue.side_effect = ValueError("Error")
    with pytest.raises(HTTPException) as exc:
        detach_ue(ue_id=1, repo=mock_repo)
    assert exc.value.status_code == 400
