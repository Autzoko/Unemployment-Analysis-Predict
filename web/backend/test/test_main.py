from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_unemployment_invalid_month():
    response = client.get("/unemployment?year=1991&month=Invalid")
    assert response.status_code == 400
    assert "Month must between 1 to 12" in response.json()["detail"]