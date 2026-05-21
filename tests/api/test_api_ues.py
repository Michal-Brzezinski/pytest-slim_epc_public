def test_list_ues_initially_empty(client):
    resp = client.get("/ues")
    assert resp.status_code == 200
    assert resp.json() == {"ues": []}

def test_attach_ue_success(client):
    resp = client.post("/ues", json={"ue_id": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"status": "attached", "ue_id": 3}

def test_attach_ue_duplicat(client):
    resp = client.post("/ues", json={"ue_id": 3})
    assert resp.status_code == 200

    resp = client.post("/ues", json={"ue_id": 3})  # 3 istnieje
    assert resp.status_code == 400
    assert resp.json()["detail"] == "UE already attached"

def test_get_attached_ue_success(client):
    resp = client.post("/ues", json={"ue_id": 3})
    assert resp.status_code == 200

    resp = client.get("/ues/3")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ue_id"] == 3

def test_get_ue_not_found(client):
    resp = client.get("/ues/3")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "UE not found"

def test_list_ues(client):
    resp = client.post("/ues", json={"ue_id": 3})
    assert resp.status_code == 200
    resp = client.post("/ues", json={"ue_id": 4})
    assert resp.status_code == 200

    resp = client.get("/ues")
    assert resp.status_code == 200
    data = resp.json()
    assert "ues" in data
    assert isinstance(data["ues"], list)
    assert set(data["ues"]) == {3, 4}

def test_detach_ue_success(client):
    resp = client.post("/ues", json={"ue_id": 3})
    assert resp.status_code == 200

    resp = client.delete("/ues/3")
    assert resp.status_code == 200
    data = resp.json()
    assert data == {"status": "detached", "ue_id": 3}

def test_detach_ue_not_found(client):
    resp = client.delete("/ues/3")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "UE not found"

def test_ues_stats_one_found(client):
    resp = client.post("/ues", json={"ue_id": 3})
    assert resp.status_code == 200
    resp = client.post("/ues", json={"ue_id": 4})
    assert resp.status_code == 200

    resp = client.get("/ues/stats?ue_id=3")
    assert resp.status_code == 200
    data = resp.json()
    assert data["scope"] == "ue:3"
    assert data["ue_count"] == 1

def test_ues_stats_all(client):
    resp = client.post("/ues", json={"ue_id": 3})
    assert resp.status_code == 200
    resp = client.post("/ues", json={"ue_id": 4})
    assert resp.status_code == 200

    resp = client.get("/ues/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert "scope" in data
    assert data["scope"] == "all"
    assert "ue_count" in data
    assert "bearer_count" in data

def test_ues_stats_notfound(client):
    resp = client.get("/ues/stats?ue_id=3")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "UE not found"

def test_attach_ue_creates_default_bearer(client):
    resp = client.post("/ues", json={"ue_id": 3})
    assert resp.status_code == 200

    resp2 = client.get("/ues/3")
    data = resp2.json()
    assert "bearers" in data
    assert "9" in data["bearers"]  # bearer 9 must exist