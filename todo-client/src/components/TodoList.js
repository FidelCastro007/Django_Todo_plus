import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../App.css';

const TodoList = () => {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [message, setMessage] = useState('');

  const fetchTasks = async () => {
    const response = await fetch('http://127.0.0.1:8000/api/tasks/');
    const data = await response.json();
    setTasks(data.tasks || []);
  };

  const handleAddTask = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/tasks/add/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description }),
      });
      const data = await response.json();
      if (response.ok) {
        fetchTasks();
        setTitle('');
        setDescription('');
        setMessage(data.message);
      } else {
        setMessage(data.error);
      }
  } catch (error) {
    setMessage('Error adding task.');
  }
};
  const handleDeleteTask = async (taskId) => {
    try {
      const response = await fetch(`/api/tasks/delete/${taskId}/`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (response.ok) {
        fetchTasks();
        setMessage(data.message);
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      setMessage('Error deleting task.');
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div className="todo-container">
      <h1>Welcome to My App!</h1>
      <p class='text-danger bg-light'>{message}</p>
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
        <button onClick={handleAddTask}>Add Task</button>
      </div>
      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id}>
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <button onClick={() => handleDeleteTask(task.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
