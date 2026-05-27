# tests/test_validation.py
def test_invalid_ue_id_range(client):
    resp = client.post("/ues", json={"ue_id": 999})
    assert resp.status_code == 422
