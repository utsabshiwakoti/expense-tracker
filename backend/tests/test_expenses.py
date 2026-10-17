from tests.conftest import make_user


def test_default_categories_seeded(client, auth):
    cats = client.get("/categories", headers=auth).json()
    assert len(cats) == 7


def test_create_and_list_expense(client, auth):
    res = client.post(
        "/expenses",
        headers=auth,
        json={"amount": 12.5, "description": "Lunch", "spent_on": "2026-10-14"},
    )
    assert res.status_code == 201
    page = client.get("/expenses", headers=auth).json()
    assert page["total"] == 1
    assert page["items"][0]["amount"] == "12.50"


def test_negative_amount_rejected(client, auth):
    res = client.post(
        "/expenses", headers=auth, json={"amount": -5, "spent_on": "2026-10-14"}
    )
    assert res.status_code == 422


def test_cannot_use_another_users_category(client, auth):
    other = make_user(client, "b@example.com")
    other_cat = client.get("/categories", headers=other).json()[0]["id"]
    res = client.post(
        "/expenses",
        headers=auth,
        json={"amount": 5, "spent_on": "2026-10-14", "category_id": other_cat},
    )
    assert res.status_code == 400


def test_users_cannot_see_each_others_expenses(client, auth):
    res = client.post(
        "/expenses", headers=auth, json={"amount": 5, "spent_on": "2026-10-14"}
    )
    expense_id = res.json()["id"]
    other = make_user(client, "b@example.com")
    assert client.get(f"/expenses/{expense_id}", headers=other).status_code == 404
    assert client.delete(f"/expenses/{expense_id}", headers=other).status_code == 404


def test_date_filter(client, auth):
    for day in ("2026-09-01", "2026-10-10"):
        client.post("/expenses", headers=auth, json={"amount": 10, "spent_on": day})
    res = client.get("/expenses", headers=auth, params={"start": "2026-10-01"})
    assert res.json()["total"] == 1
