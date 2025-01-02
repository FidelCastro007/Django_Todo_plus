import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../App.css';
import 'animate.css';

const TodoList = () => {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const [animatedTask, setAnimatedTask] = useState(null);

  // Fetch tasks from API
  const fetchTasks = async () => {
    const token = localStorage.getItem('access_token'); // JWT token from localStorage
    if (!token) {
      console.log('No token found, please log in.');
      return;
    }
    try {
      const response = await fetch('http://127.0.0.1:8000/api/tasks/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();
      if (response.ok) {
        setTasks(data.tasks || []);
      } else {
        setMessage('Failed to fetch tasks. Please log in again.');
        console.error(data);
      }
    } catch (error) {
      setMessage('Error fetching tasks.');
      console.error('Error fetching tasks:', error.message);
    }
  };

  // Add task
  const handleAddTask = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setMessage('No token found. Please log in.');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/api/tasks/add/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
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

  // Handle logout
  const handleLogout = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setMessage('No token found. Please log in.');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/api/logout/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.removeItem('access_token'); // Remove token from localStorage
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

  // Delete a task
  const handleDeleteTask = async (taskId) => {
    console.log('Deleting task with ID:', taskId); // Add this line to debug
    if (taskId === undefined) {
      setMessage('Invalid task ID');
      return;
    }
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setMessage('No token found. Please log in.');
        return;
      }
  
      const response = await fetch(`http://127.0.0.1:8000/api/tasks/delete/${taskId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
  
      // Check if the response is a JSON response
      const contentType = response.headers.get('Content-Type');
      if (contentType && contentType.includes('application/json')) {
        const data = await response.json();
        if (response.ok) {
          fetchTasks();
          setMessage(data.message || 'Task deleted successfully');
        } else {
          setMessage(data.error || 'Failed to delete task');
        }
      } else {
        // If the response isn't JSON, log an error
        setMessage('Unexpected response format. Please try again later.');
        console.error('Unexpected response:', await response.text());
      }
    } catch (error) {
      setMessage('Error deleting task.');
      console.error('Error deleting task:', error);
    }
  };
  

  // Handle editing task
  const handleEditTask = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setMessage('No token found. Please log in.');
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/tasks/edit/${editingTaskId}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
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

  // Mark task as completed
  const handleCompleteTask = async (taskId) => {
    const task = tasks.find((t) => t.id === taskId);
    if (task && task.completed) {
      setMessage('Task is already completed.');
      return; // Exit early if the task is already completed
    }
  
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setMessage('No token found. Please log in.');
        return;
      }
  
      const response = await fetch(`http://127.0.0.1:8000/api/tasks/complete/${taskId}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
  
      if (response.ok) {
        setTasks((prevTasks) =>
          prevTasks.map((task) =>
            task.id === taskId ? { ...task, completed: true } : task
          )
        );
        setAnimatedTask(taskId);
        setTimeout(() => setAnimatedTask(null), 1000);
        setMessage('Task marked as completed');
      } else {
        const data = await response.json();
        setMessage(data.error || 'Failed to mark task as completed');
      }
    } catch (error) {
      setMessage('Error completing task.');
      console.error('Error completing task:', error);
    }
  };
  
  

  // Set task details for editing
  const startEditing = (task) => {
    setEditingTaskId(task.id);
    setTitle(task.title);
    setDescription(task.description);
  };

  const getToken = () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setMessage('No token found. Please log in.');
      throw new Error('Token missing');
    }
    return token;
  };
  

  // Fetch tasks on component mount
  useEffect(() => {
    fetchTasks();
  }, []); // Empty dependency array to avoid infinite re-renders

  return (
    <div className="todo-container">
      <h1 className="animate__animated animate__bounce">Welcome to My Toddo App!</h1>
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
          <button onClick={handleEditTask} className="save-button">Update Task</button>
        ) : (
          <button onClick={handleAddTask}>Add Task</button>
        )}
      </div>

      {/* Task list */}
      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id} className={`task ${task.completed ? 'task-completed' : ''} ${animatedTask === task.id ? 'animate' : ''}`}>
          <h3>{task.title}</h3>
          <p>{task.description}</p>
          <button className="edit" onClick={() => startEditing(task)}>Edit</button>
          <button onClick={() => handleDeleteTask(task.id)}>Delete</button>
          {!task.completed && (
            <button className="complete" onClick={() => handleCompleteTask(task.id)} disabled={task.completed}>Complete</button>
          )}
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
