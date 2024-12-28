import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import 'animate.css';
import { getCsrfToken } from './csrf';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
       const csrfToken = await getCsrfToken();
        const response = await fetch('http://127.0.0.1:8000/api/login/', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({ username, password }),
        });
      const data = await response.json();
      if (response.ok) {
        // localStorage.setItem('token', data.token);
        setMessage(data.message);
        navigate('/tasks');
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      setMessage('Error during login.');
    }
  };
  

  return (
    <div className="auth-container">
      <form onSubmit={handleLogin} className="auth-form">
      <h1 className="animate__animated animate__bounce">Login</h1>
        <p className='text-danger bg-light'>{message}</p>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
        <div className="mt-3 text-center">
          <a href="/register" className="text-decoration-none" style={{ color: '#007bff' }}>
            Don't have an account? Register here
          </a>
        </div>
      </form>
    </div>
  );
};

export default Login;
