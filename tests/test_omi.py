from fastapi.testclient import TestClient


def test_search_omi_quotations_accepts_filters(client: TestClient) -> None:
    response = client.get(
        "/api/v1/omi/quotations",
        params={
            "province": "MI",
            "municipality": "Milano",
            "semester": "2025-2",
            "propertyType": "abitazioni",
            "contractType": "sale",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "source": "Agenzia Entrate - OMI",
        "query": {
            "province": "MI",
            "municipality": "Milano",
            "zone": None,
            "semester": "2025-2",
            "propertyType": "abitazioni",
            "contractType": "sale",
        },
        "results": [],
    }


def test_search_omi_quotations_validates_semester(client: TestClient) -> None:
    response = client.get(
        "/api/v1/omi/quotations",
        params={"province": "MI", "semester": "2025-3"},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
