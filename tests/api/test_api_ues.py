from pytest import fixture


@fixture
def attach_ue_id_3(client):
    resp = client.post("/ues", json={"ue_id": 3})
    assert resp.status_code == 200
    return resp

@fixture
def attach_ue_id_4(client):
    resp = client.post("/ues", json={"ue_id": 4})
    assert resp.status_code == 200
    return resp

def test_list_ues_initially_empty(client):
    resp = client.get("/ues")

    assert resp.status_code == 200
    assert resp.json() == {"ues": []}

def test_attach_ue_success(attach_ue_id_3):
    resp = attach_ue_id_3
    data = resp.json()

    assert data == {"status": "attached", "ue_id": 3}

def test_attach_ue_duplicat(client, attach_ue_id_3):
    _ = attach_ue_id_3

    resp = client.post("/ues", json={"ue_id": 3})  # 3 istnieje

    assert resp.status_code == 400
    assert resp.json()["detail"] == "UE already attached"

def test_get_attached_ue_success(client, attach_ue_id_3):
    _ = attach_ue_id_3

    resp = client.get("/ues/3")
    data = resp.json()

    assert resp.status_code == 200
    assert data["ue_id"] == 3

def test_get_ue_not_found(client):
    resp = client.get("/ues/3")

    assert resp.status_code == 400
    assert resp.json()["detail"] == "UE not found"

def test_list_ues(client, attach_ue_id_3, attach_ue_id_4):
    _ = attach_ue_id_3
    _ = attach_ue_id_4

    resp = client.get("/ues")
    data = resp.json()

    assert resp.status_code == 200
    assert "ues" in data
    assert isinstance(data["ues"], list)
    assert set(data["ues"]) == {3, 4}

def test_detach_ue_success(client, attach_ue_id_3):
    _ = attach_ue_id_3

    resp = client.delete("/ues/3")
    data = resp.json()

    assert resp.status_code == 200
    assert data == {"status": "detached", "ue_id": 3}

def test_detach_ue_not_found(client):
    resp = client.delete("/ues/3")

    assert resp.status_code == 400
    assert resp.json()["detail"] == "UE not found"

def test_ues_stats_one_found(client, attach_ue_id_3, attach_ue_id_4):
    _ = attach_ue_id_3
    _ = attach_ue_id_4

    resp = client.get("/ues/stats?ue_id=3")
    data = resp.json()

    assert resp.status_code == 200
    assert data["scope"] == "ue:3"
    assert data["ue_count"] == 1

def test_ues_stats_all(client, attach_ue_id_3, attach_ue_id_4):
    _ = attach_ue_id_3
    _ = attach_ue_id_4

    resp = client.get("/ues/stats")
    data = resp.json()

    assert resp.status_code == 200
    assert "scope" in data
    assert data["scope"] == "all"
    assert "ue_count" in data
    assert data["ue_count"] == 2
    assert "bearer_count" in data

def test_ues_stats_notfound(client):
    resp = client.get("/ues/stats?ue_id=3")

    assert resp.status_code == 400
    assert resp.json()["detail"] == "UE not found"

def test_attach_ue_creates_default_bearer(client, attach_ue_id_3):
    _ = attach_ue_id_3

    resp = client.get("/ues/3")
    data = resp.json()

    assert "bearers" in data
    assert "9" in data["bearers"]  # bearer 9 must exist