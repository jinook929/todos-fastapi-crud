import { useState, useEffect } from "react";
import api from "../api";
import AddTodoForm from "./AddTodoForm";

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editTask, setEditTask] = useState("");

  const fetchTodos = async () => {
    try {
      const response = await api.get("/todos");
      setTodos(response.data.todos);
    } catch (error) {
      console.error("Error fetching todos", error);
    }
  };

  const addTodo = async (task) => {
    try {
      await api.post("/todos", { task, completed: false });
      fetchTodos();
    } catch (error) {
      console.error(error);
    }
  };

  const updateTodo = async (id, task, completed) => {
    try {
      await api.put(`/todos/${id}`, { task, completed });
      fetchTodos();
      setEditingId(null);
    } catch (error) {
      console.error(error);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await api.delete(`/todos/${id}`);
      fetchTodos();
    } catch (error) {
      console.error(error);
    }
  };

  const toggleComplete = async (todo) => {
    await updateTodo(todo.id, todo.task, !todo.completed);
  };

  const startEdit = (todo) => {
    setEditingId(todo.id);
    setEditTask(todo.task);
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <div>
      <AddTodoForm addTodo={addTodo} />
      <h2>TODOs</h2>
      <ul>
        {todos
          .sort((a, b) => Number(a.completed) - Number(b.completed))
          .map((todo) => (
          <li key={todo.id}>
            {editingId === todo.id ? (
              <>
                <input
                  type="text"
                  value={editTask}
                  onChange={(e) => setEditTask(e.target.value)}
                />
                <span>
                  <button onClick={() => updateTodo(todo.id, editTask, todo.completed)}>Save</button>
                  <button onClick={() => setEditingId(null)}>Cancel</button>
                </span>
              </>
            ) : (
              <>
                <span style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}>
                  {todo.task}
                </span>
                <span>
                  <button onClick={() => toggleComplete(todo)}>
                    {todo.completed ? 'Undo' : 'Complete'}
                  </button>
                  <button onClick={() => startEdit(todo)}>Edit</button>
                  <button onClick={() => deleteTodo(todo.id)}>Delete</button>
                </span>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TodoList;
