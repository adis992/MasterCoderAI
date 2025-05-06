import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

function Login() {
  const { login } = useContext(AuthContext);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      navigate('/');
    } catch (err) {
      alert('Login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <form className="bg-gray-800 p-8 rounded-xl shadow-md" onSubmit={handleSubmit}>
        <h2 className="text-2xl text-white mb-4">Login</h2>
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
        <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded mb-2">Login</button>
        <p className="text-gray-400 text-sm">Don't have an account? <Link to="/register" className="text-blue-400">Register</Link></p>
      </form>
    </div>
  );
}

export default Login;