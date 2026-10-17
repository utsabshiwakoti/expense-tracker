def test_register_and_me(client):
    res = client.post(
        "/auth/register", json={"email": "a@example.com", "password": "password123"}
    )
    assert res.status_code == 201
    assert "hashed_password" not in res.json()


def test_duplicate_email_rejected(client):
    body = {"email": "a@example.com", "password": "password123"}
    client.post("/auth/register", json=body)
    assert client.post("/auth/register", json=body).status_code == 400


def test_wrong_password(client):
    client.post(
        "/auth/register", json={"email": "a@example.com", "password": "password123"}
    )
    res = client.post(
        "/auth/login", data={"username": "a@example.com", "password": "nope-nope"}
    )
    assert res.status_code == 401


def test_protected_route_needs_token(client):
    assert client.get("/expenses").status_code == 401


def test_me(client, auth):
    res = client.get("/auth/me", headers=auth)
    assert res.json()["email"] == "a@example.com"
