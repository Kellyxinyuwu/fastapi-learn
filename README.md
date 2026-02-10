# FastAPI Learning Project

A hands-on beginner project to learn the fundamentals of building REST APIs with [FastAPI](https://fastapi.tiangolo.com/). This project walks through creating a simple **Todo List API** — from setting up the environment to defining endpoints and working with data models.

---

## What This Project Covers

- Setting up a Python virtual environment
- Installing FastAPI and Uvicorn
- Creating a FastAPI application instance
- Defining routes with different HTTP methods (`GET`, `POST`)
- Using **query parameters** and **path parameters**
- Defining data models with **Pydantic** (`BaseModel`)
- Returning structured JSON responses
- Handling errors with `HTTPException`

---

## Project Structure

```
fastapi-learn/
├── main.py          # All API routes and models
├── venv/            # Python virtual environment (not committed)
└── README.md
```

---

## Getting Started

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn
```

### 3. Run the development server

```bash
uvicorn main:app --reload
```

The server starts at **http://127.0.0.1:8000**. The `--reload` flag enables auto-restart on code changes, which is great for development.

---

## API Endpoints

### `GET /` — Root

Returns a simple hello world message. Useful to verify the server is running.

```bash
curl -X GET "http://127.0.0.1:8000/"
```

**Response:**
```json
{"Hello": "World"}
```

---

### `POST /items` — Create a new item

Adds a new todo item to the in-memory list. The request body should be a JSON object matching the `Item` model.

```bash
curl -X POST "http://127.0.0.1:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"text": "Buy groceries", "is_done": false}'
```

**Response:** Returns the full items list after adding the new item.

---

### `GET /items` — List all items

Returns items from the list. Accepts an optional `limit` query parameter (defaults to 10).

```bash
# Use default limit (10)
curl -X GET "http://127.0.0.1:8000/items"

# Specify a custom limit
curl -X GET "http://127.0.0.1:8000/items?limit=5"
```

**Response:**
```json
[
  {"text": "Buy groceries", "is_done": false},
  {"text": "Walk the dog", "is_done": true}
]
```

---

### `GET /items/{item_id}` — Get a specific item

Retrieves a single item by its index in the list. Returns a `404` error if the index is out of range.

```bash
curl -X GET "http://127.0.0.1:8000/items/0"
```

**Response:**
```json
{"text": "Buy groceries", "is_done": false}
```

**Error response (item not found):**
```json
{"detail": "Item id 99 not found"}
```

---

## Key Concepts Learned

### FastAPI App Instance
```python
from fastapi import FastAPI
app = FastAPI()
```
This creates the application. All routes are registered on this `app` object using decorators like `@app.get()` and `@app.post()`.

### Route vs Endpoint

These two terms are related but mean slightly different things:

- **Route** — the URL **path** defined in the decorator, e.g. `/items`. It's the URL pattern that maps to a function.
- **Endpoint** — the combination of the **path + HTTP method**, e.g. `POST /items`. This is what uniquely identifies where a request goes.

You can have two routes with the **same path** but different methods, and they are **different endpoints**:

```python
@app.post("/items")   # Endpoint: POST /items
def create_item(...):

@app.get("/items")    # Endpoint: GET /items
def list_items(...):
```

Same route (`/items`), two different endpoints. In everyday conversation people use the terms interchangeably — and that's fine — but technically, **endpoint = route + HTTP method**.

### Route Decorators
- `@app.get("/path")` — handles HTTP GET requests
- `@app.post("/path")` — handles HTTP POST requests

The path string defines the URL endpoint. FastAPI automatically generates interactive API docs at `/docs`.

### Query Parameters vs Path Parameters
- **Query parameters** are appended to the URL after `?` (e.g., `/items?limit=5`). They are defined as function arguments with default values.
- **Path parameters** are part of the URL path (e.g., `/items/{item_id}`). They are defined using curly braces in the route and as function arguments.

### Pydantic Models
```python
from pydantic import BaseModel

class Item(BaseModel):
    text: str = None
    is_done: bool = False
```
Pydantic models define the shape of request/response data. FastAPI uses them to automatically validate incoming JSON, generate documentation, and serialize responses.

### Error Handling
```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Item not found")
```
Raises a proper HTTP error response when something goes wrong, like requesting an item that doesn't exist.

---

## Interactive API Docs

FastAPI auto-generates interactive documentation based on your code — your route decorators, type hints, and Pydantic models are all used to build it automatically. No extra configuration needed.

### How to Open the Interactive Docs

**Step 1:** Make sure your virtual environment is activated:

```bash
source venv/bin/activate
```

**Step 2:** Start the server (and keep it running):

```bash
uvicorn main:app --reload
```

**Step 3:** With the server running, open one of these URLs in your browser:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

The server must stay running in the terminal while you use the docs. If you stop the server (Ctrl+C), the docs page will stop working.

### Why Use Interactive Docs Instead of the Terminal?

Testing APIs with `curl` in the terminal works, but it has friction:

- You have to remember the exact URL, method, headers, and body format
- Long commands are easy to mistype (wrong port, line breaks, missing quotes)
- You can't easily see what parameters an endpoint expects

The **Swagger UI** solves all of this:

| | Terminal (`curl`) | Swagger UI (`/docs`) |
|---|---|---|
| **See all endpoints** | You need to read the code | Listed visually in one page |
| **Know the parameters** | You need to read the code | Auto-generated input forms |
| **Send a request** | Type a full curl command | Click "Try it out" and fill in fields |
| **See the response** | Raw text in terminal | Formatted JSON with status code |
| **Error-prone?** | Easy to mistype URLs, ports, JSON | Point-and-click, minimal errors |
| **Request body format** | You must know the JSON structure | Shows the exact schema from your Pydantic model |

In short, **Swagger UI is like a visual, interactive version of curl** — it reads your code and builds a UI for testing, so you don't have to memorize anything.

### Swagger UI vs ReDoc

Both are auto-generated from the same code, but they serve different purposes:

| | Swagger UI (`/docs`) | ReDoc (`/redoc`) |
|---|---|---|
| **Can test endpoints?** | Yes — "Try it out" button lets you send real requests | No — read-only, documentation viewing only |
| **Best for** | Development and debugging — quickly test your API while building it | Sharing — clean, polished docs to give to teammates or API consumers |
| **Layout** | Functional, collapsible sections per endpoint | Clean, three-panel layout with search and navigation sidebar |
| **Shows request body schema?** | Yes, with editable example JSON | Yes, with detailed model breakdowns |
| **Interactive?** | Fully interactive — fill in fields, click execute, see live response | Not interactive — purely for reading |

**When to use which:**
- Use **Swagger UI** (`/docs`) during development. It's your go-to tool for testing endpoints without leaving the browser.
- Use **ReDoc** (`/redoc`) when you want to share clean API documentation with others, or when you just want to read through your API's structure.

---

## Notes

- Items are stored **in memory** (a Python list). Restarting the server clears all data. In a real application, you would use a database.
- Always make sure to add items (`POST /items`) before trying to retrieve them (`GET /items` or `GET /items/{item_id}`).
