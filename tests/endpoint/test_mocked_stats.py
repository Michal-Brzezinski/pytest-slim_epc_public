import pytest
from fastapi import HTTPException
from epc.api import get_ues_stats
from epc.models import UEState, BearerConfig, ThroughputStats

def test_get_ues_stats_ue_not_exists_given(mock_repo):
    mock_repo.ue_exists.return_value = False
    with pytest.raises(HTTPException) as exc:
        get_ues_stats(repo=mock_repo, ue_id=1)
    assert exc.value.status_code == 400

def test_get_ues_stats_ue_get_value_error_explicit(mock_repo):
    mock_repo.ue_exists.return_value = True
    mock_repo.get_ue.side_effect = ValueError()
    with pytest.raises(HTTPException) as exc:
        get_ues_stats(repo=mock_repo, ue_id=1)
    assert exc.value.status_code == 400

def test_get_ues_stats_ue_get_value_error_implicit(mock_repo, mock_tm):
    """Gałąź, w której repo z wraca błąd dla konkretnego elementu listy i system pomija ten element (continue)."""
    mock_repo.list_ues.return_value = [1, 2]
    
    def side_effect(uid):
        if uid == 1:
            raise ValueError()
        return UEState(ue_id=2)
    
    mock_repo.get_ue.side_effect = side_effect
    response = get_ues_stats(repo=mock_repo, ue_id=None, include_details=False)
    assert response.ue_count == 2

