def test_root_healthcheck(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "EPC Simulator running"}
