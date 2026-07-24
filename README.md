# To-Do CRUD API

This is a clean RESTful CRUD API built with Python and FastAPI that manages a persistent to-do list using a SQLite database. It was built as part of an exercise to master the fundamentals of backend development, handling the complete request → response loop and all four CRUD operations.

## Why SQLite?
SQLite is a lightweight SQL database that stores data in a single file on your computer. It requires no separate server to run, making it perfect for small to medium applications and learning relational databases. It persists our data across server restarts while maintaining a minimal setup.

## Database Location
The database is stored in a single file named `tasks.db` located in the root of this project. It will be automatically created the first time you run the application.

## How to Install & Run

You can start the server locally in under a minute.

1. **Install Dependencies:**
   ```bash
   pip install fastapi uvicorn
   ```
   *(Note: SQLite is included in Python's standard library, so no extra database packages are needed!)*

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

## Exploring the Database Manually

You can use a tool like [DB Browser for SQLite](https://sqlitebrowser.org/) to open `tasks.db` and manually run SQL queries. For example, to list all tasks:

```sql
SELECT * FROM tasks;
```

To see only completed tasks:

```sql
SELECT * FROM tasks WHERE done = 1;
```

### Database Screenshot
*(Please replace this text with a screenshot of your SQLite database viewer showing the `tasks` table)*

## Swagger UI

*(Please replace this text with a screenshot of your Swagger UI at `http://localhost:8000/docs`)*
