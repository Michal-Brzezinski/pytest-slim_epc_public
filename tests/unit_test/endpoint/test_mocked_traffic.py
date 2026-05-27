import time
import pytest
from fastapi import HTTPException
from epc.api import start_traffic, stop_traffic, get_traffic_stats
from epc.models import UEState, BearerConfig, ThroughputStats, StartTrafficRequest

def test_start_traffic_ue_value_error(mock_repo):
    mock_repo.get_ue.side_effect = ValueError("err")
    with pytest.raises(HTTPException) as exc:
        start_traffic(ue_id=1, bearer_id=5, body=StartTrafficRequest(protocol="udp", Mbps=1.0), repo=mock_repo)
    assert exc.value.status_code == 400

def test_start_traffic_bearer_not_found(mock_repo):
    mock_repo.get_ue.return_value = UEState(ue_id=1, bearers={})
    with pytest.raises(HTTPException) as exc:
        start_traffic(ue_id=1, bearer_id=5, body=StartTrafficRequest(protocol="udp", Mbps=1.0), repo=mock_repo)
    assert exc.value.status_code == 400

def test_start_traffic_existing_stats(mock_repo, mock_tm):
    state = UEState(
        ue_id=1,
        bearers={5: BearerConfig(bearer_id=5)},
        stats={5: ThroughputStats(bearer_id=5, ue_id=1)}
    )
    mock_repo.get_ue.return_value = state
    response = start_traffic(ue_id=1, bearer_id=5, body=StartTrafficRequest(protocol="udp", Mbps=1.0), repo=mock_repo)
    assert response.status == "traffic_started"
    mock_repo.update_stats.assert_not_called()

def test_start_traffic_tm_value_error(mock_repo, mock_tm):
    state = UEState(ue_id=1, bearers={5: BearerConfig(bearer_id=5)}, stats={})
    mock_repo.get_ue.return_value = state
    mock_tm.start.side_effect = ValueError("err")
    with pytest.raises(HTTPException) as exc:
        start_traffic(ue_id=1, bearer_id=5, body=StartTrafficRequest(protocol="udp", Mbps=1.0), repo=mock_repo)
    assert exc.value.status_code == 400

def test_stop_traffic_ue_value_error(mock_repo):
    mock_repo.get_ue.side_effect = ValueError("err")
    with pytest.raises(HTTPException) as exc:
        stop_traffic(ue_id=1, bearer_id=5, repo=mock_repo)
    assert exc.value.status_code == 400

def test_stop_traffic_bearer_not_found(mock_repo):
    mock_repo.get_ue.return_value = UEState(ue_id=1, bearers={})
    with pytest.raises(HTTPException) as exc:
        stop_traffic(ue_id=1, bearer_id=5, repo=mock_repo)
    assert exc.value.status_code == 400

def test_get_traffic_stats_ue_error(mock_repo):
    mock_repo.get_ue.side_effect = ValueError("Error")
    with pytest.raises(HTTPException) as exc:
        get_traffic_stats(ue_id=1, bearer_id=5, repo=mock_repo)
    assert exc.value.status_code == 400

def test_get_traffic_stats_no_stats(mock_repo):
    mock_repo.get_ue.return_value = UEState(
        ue_id=1, bearers={5: BearerConfig(bearer_id=5)}
    )
    response = get_traffic_stats(ue_id=1, bearer_id=5, repo=mock_repo)
    assert response.tx_bps == 0
    assert response.rx_bps == 0
    assert response.duration == 0

