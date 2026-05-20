# tests/test_api_traffic.py
def test_start_and_stop_traffic(client):
    client.post("/ues", json={"ue_id": 1})
    client.post("/ues/1/bearers", json={"bearer_id": 1})

    resp = client.post("/ues/1/bearers/1/traffic",
                       json={"protocol": "tcp", "Mbps": 1})
    assert resp.status_code == 200

    resp2 = client.delete("/ues/1/bearers/1/traffic")
    assert resp2.status_code == 200
