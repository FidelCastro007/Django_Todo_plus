import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import 'animate.css';
import { getCsrfToken } from './csrf';

const TodoList = () => {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [editingTaskId, setEditingTaskId] = useState(null);
  const navigate = useNavigate();
  const [message, setMessage] = useState('');

  // Fetch tasks from API
  const fetchTasks = async () => {
    try {
      const csrfToken = await getCsrfToken(); // Get CSRF token
      const response = await fetch('http://127.0.0.1:8000/api/tasks/', {
        method: 'GET',
        headers: { 'X-CSRFToken': csrfToken }, // CSRF token for authentication
        credentials: 'include',
      });

      const data = await response.json();
      if (response.ok) {
        setTasks(data.tasks || []);
      } else {
        setMessage('Failed to fetch tasks. Please log in again.');
        // navigate('/login')
        console.error(data);
      }
    } catch (error) {
      setMessage('Error fetching tasks.');
      console.error('Error fetching tasks:', error.message);
    }
  };

  // Add a new task
  const handleAddTask = async () => {
    try {
      const csrfToken = await getCsrfToken(); // Get CSRF token
      const response = await fetch('http://127.0.0.1:8000/api/tasks/add/', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // CSRF token for authentication
        },
        body: JSON.stringify({ title, description }),
      });

      const data = await response.json();
      if (response.ok) {
        fetchTasks();
        setTitle('');
        setDescription('');
        setMessage(data.message || 'Task added successfully');
      } else {
        setMessage(data.error || 'Failed to add task');
      }
    } catch (error) {
      setMessage('Error adding task.');
      console.error('Error adding task:', error);
    }
  };

  // Delete a task
  const handleDeleteTask = async (taskId) => {
    try {
      const csrfToken = await getCsrfToken(); // Get CSRF token
      const response = await fetch(`http://127.0.0.1:8000/api/tasks/delete/${taskId}/`, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': csrfToken, // CSRF token for authentication
        },
      });

      const data = await response.json();
      if (response.ok) {
        fetchTasks();
        setMessage(data.message || 'Task deleted successfully');
      } else {
        setMessage(data.error || 'Failed to delete task');
      }
    } catch (error) {
      setMessage('Error deleting task.');
      console.error('Error deleting task:', error);
    }
  };

  // Handle editing task
  const handleEditTask = async () => {
    try {
      const csrfToken = await getCsrfToken(); // Get CSRF token
      const response = await fetch(`http://127.0.0.1:8000/api/tasks/edit/${editingTaskId}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // CSRF token for authentication
        },
        body: JSON.stringify({ title, description }),
      });

      const data = await response.json();
      if (response.ok) {
        fetchTasks();
        setTitle('');
        setDescription('');
        setEditingTaskId(null);
        setMessage(data.message || 'Task updated successfully');
      } else {
        setMessage(data.error || 'Failed to update task');
      }
    } catch (error) {
      setMessage('Error updating task.');
      console.error('Error updating task:', error);
    }
  };

  // Set task details for editing
  const startEditing = (task) => {
    setEditingTaskId(task.id);
    setTitle(task.title);
    setDescription(task.description);
  };

  // Handle logout
  const handleLogout = async () => {
    try {
      const csrfToken = await getCsrfToken(); // Get CSRF token
      const response = await fetch('http://127.0.0.1:8000/api/logout/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken, // CSRF token for authentication
        },
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.removeItem('token'); // Clear token if stored locally
        navigate('/login');
        setMessage(data.message || 'Successfully logged out');
      } else {
        setMessage(data.error || 'Failed to log out');
      }
    } catch (error) {
      setMessage('Error logging out.');
      console.error('Error logging out:', error);
    }
  };

  // Fetch tasks on component mount
  useEffect(() => {
    fetchTasks();
  }, []); // Empty dependency array to avoid infinite re-renders

  return (
    <div className="todo-container">
      <h1 className="animate__animated animate__bounce">Welcome to My App!</h1>
      <p className="text-danger bg-light">{message}</p>

      {/* Form for adding or editing tasks */}
      <div className="task-input">
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
        {editingTaskId ? (
          <button onClick={handleEditTask}>Update Task</button>
        ) : (
          <button onClick={handleAddTask}>Add Task</button>
        )}
      </div>

      {/* Task list */}
      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id}>
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <button onClick={() => startEditing(task)}>Edit</button>
            <button onClick={() => handleDeleteTask(task.id)}>Delete</button>
          </li>
        ))}
      </ul>

      {/* Logout button */}
      <div className="logout">
        <button onClick={handleLogout}>Logout</button>
      </div>
    </div>
  );
};

export default TodoList;
