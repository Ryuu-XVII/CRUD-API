import sqlite3
from fastapi import FastAPI, status, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

DB_FILE = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    
    # Insert example tasks if the table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    if count == 0:
        example_tasks = [
            ("Buy groceries", False),
            ("Read a book", True),
            ("Write some code", False)
        ]
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", example_tasks)
        
    conn.commit()
    conn.close()
    
    yield
    # Shutdown logic (if any)

app = FastAPI(
    title="Task API",
    description="A clean, production-ready RESTful CRUD API for managing a to-do list.",
    version="1.0",
    lifespan=lifespan
)

# Standard CORS setup for production readiness
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def find_task(task_id: int):
    """Helper to locate a task by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def format_task(task: dict):
    """Ensure boolean mapping for 'done' as SQLite stores it as 0/1."""
    if task:
        task["done"] = bool(task["done"])
    return task

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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [format_task(dict(row)) for row in rows]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Retrieves a specific task by its ID."""
    task = find_task(task_id)
    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    return format_task(task)

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: dict = Body(default={})):
    """Creates a new task. Requires a 'title' in the JSON body."""
    title = payload.get("title")
    if title is None or not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing 'title'. It must be a non-empty string."}
        )
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title.strip(), False))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return format_task(find_task(new_id))

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
    
    update_title = task["title"]
    update_done = task["done"]
    
    if "title" in payload:
        title = payload["title"]
        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "If provided, 'title' must be a non-empty string."}
            )
        update_title = title.strip()
        
    if "done" in payload:
        done = payload["done"]
        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "If provided, 'done' must be a boolean."}
            )
        update_done = done
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (update_title, update_done, task_id)
    )
    conn.commit()
    conn.close()
    
    return format_task(find_task(task_id))

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Deletes a task by its ID."""
    task = find_task(task_id)
    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    return None
