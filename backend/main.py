import uvicorn
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import contextmanager

class Todo(BaseModel):
    id: int | None = None
    task: str
    completed: bool = False

class Todos(BaseModel):
    todos: list[Todo]

DB_PATH = "todos.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS todos
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         task TEXT NOT NULL,
         completed BOOLEAN NOT NULL DEFAULT 0)
        ''')
        conn.commit()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "http://localhost:3030",
    "https://jinookjung.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/todos", response_model=Todos)
def get_todos():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, completed FROM todos")
        todos = [{"id": row[0], "task": row[1], "completed": bool(row[2])} for row in cursor.fetchall()]
        return Todos(todos=todos)

@app.post("/todos", response_model=Todo)
def add_todo(todo: Todo):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (task, completed) VALUES (?, ?)", (todo.task, todo.completed))
        conn.commit()
        return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET task = ?, completed = ? WHERE id = ?", (todo.task, todo.completed, todo_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Todo not found")
        conn.commit()
        cursor.execute("SELECT id, task, completed FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        return Todo(id=row[0], task=row[1], completed=bool(row[2]))

@app.delete("/todos/{todo_id}", response_model=Todos)
def delete_todo(todo_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Todo not found")
        conn.commit()
        return get_todos()

def seed_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM todos")
        if cursor.fetchone()[0] == 0:
            initial_todos = [
                ("Learn FastAPI", False),
                ("Build Todo App", False),
                ("Write Tests", False)
            ]
            cursor.executemany("INSERT INTO todos (task, completed) VALUES (?, ?)", initial_todos)
            conn.commit()

@app.on_event("startup")
async def startup():
    init_db()
    seed_db()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)