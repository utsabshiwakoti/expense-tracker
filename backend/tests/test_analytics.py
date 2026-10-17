def test_summary_and_by_category(client, auth):
    food = next(
        c["id"] for c in client.get("/categories", headers=auth).json()
        if c["name"] == "Food"
    )
    client.post("/expenses", headers=auth,
                json={"amount": 10, "spent_on": "2026-10-01", "category_id": food})
    client.post("/expenses", headers=auth,
                json={"amount": 30, "spent_on": "2026-10-02"})

    summary = client.get("/analytics/summary", headers=auth).json()
    assert summary["total"] == "40.00"
    assert summary["count"] == 2

    rows = client.get("/analytics/by-category", headers=auth).json()
    names = {r["category"]: r["total"] for r in rows}
    assert names == {"Food": "10.00", "Uncategorized": "30.00"}


def test_monthly_fills_empty_months(client, auth):
    rows = client.get("/analytics/monthly", headers=auth, params={"months": 3}).json()
    assert len(rows) == 3
    assert all(r["total"] == "0.00" for r in rows)
