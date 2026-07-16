# To-Do CRUD API

This is a clean, single-file RESTful CRUD API built with Python and FastAPI that manages an in-memory to-do list. It was built as part of an exercise to master the fundamentals of backend development, handling the complete request → response loop and all four CRUD operations.

## How to Install & Run

You can start the server locally in under a minute.

1. **Install Dependencies:**
   ```bash
   pip install fastapi uvicorn
   ```

2. **Start the Server:**
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints

| CRUD operation | HTTP method | Endpoint | Meaning |
|---|---|---|---|
| Read (Meta) | `GET` | `/` | Returns metadata about the API |
| Read (Health) | `GET` | `/health` | Returns the health status of the API |
| Read (All) | `GET` | `/tasks` | List all tasks |
| Read (Single) | `GET` | `/tasks/{id}` | Get a specific task by its ID |
| Create | `POST` | `/tasks` | Add a new task (requires JSON body) |
| Update | `PUT` | `/tasks/{id}` | Update an existing task's title or status |
| Delete | `DELETE` | `/tasks/{id}` | Remove a task by its ID |

## Example Request (curl)

Here is an example of creating a new task using `curl`:

```bash
$ curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'

HTTP/1.1 201 Created
date: Thu, 16 Jul 2026 10:00:00 GMT
server: uvicorn
content-length: 44
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

*(Please replace this text with a screenshot of your Swagger UI at `http://localhost:8000/docs`)*
