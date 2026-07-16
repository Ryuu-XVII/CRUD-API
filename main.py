from fastapi import FastAPI, status, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Task API",
    description="A clean, production-ready RESTful CRUD API for managing a to-do list.",
    version="1.0"
)

# Standard CORS setup for production readiness
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data store with 3 pre-filled task objects
tasks_db = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book", "done": True},
    {"id": 3, "title": "Write some code", "done": False}
]

def find_task(task_id: int):
    """Helper to locate a task by ID."""
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    return None

@app.get("/")
def read_root():
    """Returns metadata about the API."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    """Returns the health status of the API."""
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    """Retrieves all tasks in the database."""
    return tasks_db

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Retrieves a specific task by its ID."""
    task = find_task(task_id)
    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    return task

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: dict = Body(default={})):
    """Creates a new task. Requires a 'title' in the JSON body."""
    title = payload.get("title")
    if title is None or not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing 'title'. It must be a non-empty string."}
        )
    
    new_id = max((t["id"] for t in tasks_db), default=0) + 1
    new_task = {
        "id": new_id,
        "title": title.strip(),
        "done": False
    }
    tasks_db.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: dict = Body(default={})):
    """Updates an existing task. Replaces 'title' and/or 'done' status."""
    if not payload:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty."}
        )
    
    task = find_task(task_id)
    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    
    if "title" in payload:
        title = payload["title"]
        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "If provided, 'title' must be a non-empty string."}
            )
        task["title"] = title.strip()
        
    if "done" in payload:
        done = payload["done"]
        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "If provided, 'done' must be a boolean."}
            )
        task["done"] = done
        
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Deletes a task by its ID."""
    task = find_task(task_id)
    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    
    tasks_db.remove(task)
    return None
