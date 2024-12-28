import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import 'animate.css';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage('Registration successful! Please login.');
        navigate('/login');
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      setMessage('Error during registration.');
  };
};

  return (
    <div className="auth-container">
      <form onSubmit={handleRegister} className="auth-form">
      <h2 className="animate__animated animate__bounce">Register</h2>
        <p className='text-danger bg-light'>{message}</p>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
          <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Register</button>
        <div className="mt-3 text-center">
          <a href="/login" className="text-decoration-none">
            ← Back to Login
          </a>
        </div>
      </form>
    </div>
  );
};

export default Register;
