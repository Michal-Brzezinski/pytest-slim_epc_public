from pytest import fixture


@fixture
def attach_bearer_id_7_to_ue_id_3(client):
    client.post("/ues", json={"ue_id": 3})
    resp = client.post("/ues/3/bearers", json={"bearer_id": 7})
    return resp

def test_add_bearer(client, attach_bearer_id_7_to_ue_id_3):
    resp = attach_bearer_id_7_to_ue_id_3
    data = resp.json()

    resp_get = client.get("/ues/3")
    data_get = resp_get.json()

    assert resp.status_code == 200
    assert data == {'status': 'bearer_added', 'ue_id': 3, 'bearer_id': 7}
    assert "bearers" in data_get
    assert "7" in data_get["bearers"]

def test_add_bearer_duplicate(client, attach_bearer_id_7_to_ue_id_3):
    _ = attach_bearer_id_7_to_ue_id_3

    resp = client.post("/ues/3/bearers", json={"bearer_id": 7})  # 7 już istnieje

    assert resp.status_code == 400
    assert resp.json()["detail"] == "Bearer already exists"

def test_delete_bearer_success(client, attach_bearer_id_7_to_ue_id_3):
    _ = attach_bearer_id_7_to_ue_id_3

    resp_delete = client.delete("/ues/3/bearers/7")
    resp_get = client.get("/ues/3")
    data = resp_get.json()

    assert resp_delete.status_code == 200
    assert resp_delete.json()["status"] == "bearer_deleted"
    assert 7 not in data["bearers"]

def test_delete_bearer_not_found(client):
    client.post("/ues", json={"ue_id": 3})

    resp = client.delete("/ues/3/bearers/7")

    assert resp.status_code == 400
    assert resp.json()["detail"] == "Bearer not found"

def test_delete_bearer_default_forbidden(client):
    client.post("/ues", json={"ue_id": 3})

    resp = client.delete("/ues/3/bearers/9")

    assert resp.status_code == 400
    assert resp.json()["detail"] == "Cannot remove default bearer"
