import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/auth/register', { username, password });
      alert('Registration successful, please login');
      navigate('/login');
    } catch (err) {
      alert('Registration failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <form className="bg-gray-800 p-8 rounded-xl shadow-md" onSubmit={handleSubmit}>
        <h2 className="text-2xl text-white mb-4">Register</n2>
        <input
          className="w-full mb-2 p-2 rounded bg-gray-700 text-white"
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          className="w-full mb-4 p-2 rounded bg-gray-700 text-white"
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded mb-2">Register</button>
        <p className="text-gray-400 text-sm">Already have an account? <Link to="/login" className="text-blue-400">Login</Link></p>
      </form>
    </div>
  );
}

export default Register;