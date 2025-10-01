from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_and_order_flow():
    # login
    r = client.post("/auth/login", json={"username":"admin","password":"secret"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create order
    r = client.post("/v1/orders", json={"customer_id":"c1","items":[{"sku":"A","qty":1,"price":10}]}, headers=headers)
    assert r.status_code == 201
    oid = r.json()["id"]

    # get order
    r = client.get(f"/v1/orders/{oid}", headers=headers)
    assert r.status_code == 200
    assert r.json()["customer_id"] == "c1"
