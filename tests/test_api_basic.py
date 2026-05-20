# tests/test_api_basic.py
def test_root_healthcheck(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "EPC Simulator running"}

def test_list_ues_initially_empty(client):
    resp = client.get("/ues")
    assert resp.status_code == 200
    assert resp.json() == {"ues": []}

def test_attach_ue_creates_default_bearer(client):
    resp = client.post("/ues", json={"ue_id": 1})
    assert resp.status_code == 200
    assert resp.json() == {"status": "attached", "ue_id": 1}

    resp2 = client.get("/ues/1")
    data = resp2.json()
    assert "bearers" in data
    assert "9" in data["bearers"]  # bearer 9 must exist
