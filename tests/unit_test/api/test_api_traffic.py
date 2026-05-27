from pytest import fixture


@fixture(autouse=True)
def cleanup_stuff(client):
    yield
    client.post("/reset")

def test_start_traffic_udp_bps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})

    resp = client.post("/ues/3/bearers/7/traffic", json={"protocol": "udp", "bps": 9000})
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_started"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7
    assert data["target_bps"] == 9000

def test_start_traffic_udp_kbps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})

    resp = client.post("/ues/3/bearers/7/traffic", json={"protocol": "udp", "kbps": 9})
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_started"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7
    assert data["target_bps"] == 9000

def test_start_traffic_udp_mbps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})

    resp = client.post("/ues/3/bearers/7/traffic", json={"protocol": "udp", "Mbps": 9})
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_started"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7
    assert data["target_bps"] == 9_000_000

def test_start_traffic_tcp_bps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})

    resp = client.post("/ues/3/bearers/7/traffic", json={"protocol": "tcp", "bps": 9000})
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_started"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7
    assert data["target_bps"] == 9000

def test_start_traffic_tcp_kbps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})

    resp = client.post("/ues/3/bearers/7/traffic", json={"protocol": "tcp", "kbps": 9})
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_started"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7
    assert data["target_bps"] == 9000

def test_start_traffic_tcp_mbps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})

    resp = client.post("/ues/3/bearers/7/traffic", json={"protocol": "tcp", "Mbps": 9})
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_started"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7
    assert data["target_bps"] == 9_000_000

def test_start_traffic_mbps_and_bps_fail(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})

    resp = client.post("/ues/3/bearers/7/traffic", json={"protocol": "tcp", "Mbps": 9, "bps": 9000})
    data = resp.json()

    assert resp.status_code == 422
    assert "detail" in data
    assert data["detail"][0]["type"] == "value_error"
    assert data["detail"][0]["msg"] == "Value error, Provide exactly one throughput value (Mbps, kbps, or bps)"

def test_start_traffic_not_found_ue(client):
    resp = client.post("/ues/3/bearers/7/traffic", json={"protocol": "udp", "bps": 9000})

    assert resp.status_code == 400
    assert "not found" in resp.json()["detail"]

def test_start_traffic_bearer_not_found(client):
    client.post("/ues", json={"ue_id": 3})

    resp = client.post("/ues/3/bearers/7/traffic", json={"protocol": "udp", "bps": 9000})

    assert resp.status_code == 400
    assert "Bearer not found" in resp.json()["detail"]

def test_stop_traffic_udp_bps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})
    client.post("/ues/3/bearers/7/traffic", json={"protocol": "udp", "bps": 9000})

    resp = client.delete("/ues/3/bearers/7/traffic")
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_stopped"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7

def test_stop_traffic_udp_kbps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})
    client.post("/ues/3/bearers/7/traffic", json={"protocol": "udp", "kbps": 9})

    resp = client.delete("/ues/3/bearers/7/traffic")
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_stopped"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7

def test_stop_traffic_udp_mbps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})
    client.post("/ues/3/bearers/7/traffic", json={"protocol": "udp", "Mbps": 9})

    resp = client.delete("/ues/3/bearers/7/traffic")
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_stopped"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7


def test_stop_traffic_tcp_bps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})
    client.post("/ues/3/bearers/7/traffic", json={"protocol": "tcp", "bps": 9000})

    resp = client.delete("/ues/3/bearers/7/traffic")
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_stopped"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7


def test_stop_traffic_tcp_kbps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})
    client.post("/ues/3/bearers/7/traffic", json={"protocol": "tcp", "kbps": 9})

    resp = client.delete("/ues/3/bearers/7/traffic")
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_stopped"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7


def test_stop_traffic_tcp_mbps_success(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})
    client.post("/ues/3/bearers/7/traffic", json={"protocol": "tcp", "Mbps": 9})

    resp = client.delete("/ues/3/bearers/7/traffic")
    data = resp.json()

    assert resp.status_code == 200
    assert data["status"] == "traffic_stopped"
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7

def test_stop_traffic_ue_not_found(client, test_repo):
    resp = client.delete("/ues/3/bearers/7/traffic")

    assert resp.status_code == 400
    assert "not found" in resp.json()["detail"]

def test_stop_traffic_bearer_not_found(client):
    client.post("/ues", json={"ue_id": 3})

    resp = client.delete("/ues/3/bearers/7/traffic")
    assert resp.status_code == 400
    assert "Bearer not found" in resp.json()["detail"]

def test_get_traffic_stats_none(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})

    resp = client.get("/ues/3/bearers/7/traffic")
    data = resp.json()

    assert resp.status_code == 200
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7
    assert data["protocol"] is None
    assert data["target_bps"] is None
    assert data["tx_bps"] == 0
    assert data["rx_bps"] == 0
    assert data["duration"] == 0

def test_get_traffic_stats_value(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues/3/bearers", json={"bearer_id": 7})
    client.post("/ues/3/bearers/7/traffic", json={"protocol": "udp", "bps": 9000})

    resp = client.get("/ues/3/bearers/7/traffic")
    data = resp.json()

    assert resp.status_code == 200
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7
    assert data["tx_bps"] >= 0
    assert data["rx_bps"] >= 0
    assert data["duration"] >= 0
    assert data["protocol"] == "udp"
    assert data["target_bps"] == 9000

def test_get_traffic_stats_ue_not_found(client):
    resp = client.get("/ues/3/bearers/7/traffic")

    assert resp.status_code == 400
    assert "not found" in resp.json()["detail"]

def test_get_traffic_stats_bearer_not_exist(client):
    client.post("/ues", json={"ue_id": 3})

    resp = client.get("/ues/3/bearers/7/traffic")
    data = resp.json()

    assert resp.status_code == 200
    assert data["ue_id"] == 3
    assert data["bearer_id"] == 7
    assert data["protocol"] is None
    assert data["target_bps"] is None
    assert data["tx_bps"] == 0
    assert data["rx_bps"] == 0
    assert data["duration"] == 0
