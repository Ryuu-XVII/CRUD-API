from fastapi.testclient import TestClient
from main import app
import os

if os.path.exists("tasks.db"):
    os.remove("tasks.db")

client = TestClient(app)

with client:
    # Test read all
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 3
    print("GET /tasks OK")
    
    # Test read single
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Buy groceries"
    print("GET /tasks/1 OK")
    
    # Test create
    response = client.post("/tasks", json={"title": "Test persistence"})
    assert response.status_code == 201
    new_id = response.json()["id"]
    print(f"POST /tasks OK, new ID: {new_id}")
    
    # Test update
    response = client.put(f"/tasks/{new_id}", json={"done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True
    print(f"PUT /tasks/{new_id} OK")
    
    # Test delete
    response = client.delete("/tasks/2")
    assert response.status_code == 204
    print("DELETE /tasks/2 OK")
    
# Re-init client to test persistence
client2 = TestClient(app)
with client2:
    response = client2.get("/tasks")
    tasks = response.json()
    assert len(tasks) == 3 # 3 init + 1 create - 1 delete = 3
    titles = [t["title"] for t in tasks]
    assert "Test persistence" in titles
    assert "Read a book" not in titles
    print("Persistence OK")
    
print("All tests passed!")
