def test_root_healthcheck(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "EPC Simulator running"}

def test_reset_all(client):
    client.post("/ues", json={"ue_id": 3})
    client.post("/ues", json={"ue_id": 4})
    client.post("/ues/3/bearers/9/traffic", json={"protocol": "udp", "bps": 9000})

    resp_reset = client.post("/reset")
    resp_get_ues = client.get("/ues")

    assert resp_reset.status_code == 200
    assert resp_reset.json() == {"status": "reset"}
    assert resp_get_ues.json() == {"ues": []}

