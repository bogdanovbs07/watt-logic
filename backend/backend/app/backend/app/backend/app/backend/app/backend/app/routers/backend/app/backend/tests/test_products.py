from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_products_no_params():
    response = client.get("/products/")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert "count" in json_data
    assert json_data["count"] == 3  # Три наших тестовых товара
