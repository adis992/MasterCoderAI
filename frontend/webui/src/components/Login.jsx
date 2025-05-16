import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

function Login() {
  const { login } = useContext(AuthContext);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password, remember);
      setError('');
      // Redirect to root, let App.js handle admin vs. user routes
      navigate('/', { replace: true });
    } catch (err) {
      // Display error message
      const msg = err.response?.data?.detail || err.message || 'Login failed';
      setError(msg);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <form className="bg-gray-800 p-8 rounded-xl shadow-lg w-full max-w-sm mx-auto text-center" onSubmit={handleSubmit}>
        <h2 className="text-2xl text-white mb-6 font-bold">Login</h2>
        {error && <div className="text-red-400 mb-2">{error}</div>}
        <input
          className="w-full mb-4 p-2 rounded bg-gray-700 text-white text-center placeholder-gray-400"
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          className="w-full mb-4 p-2 rounded bg-gray-700 text-white text-center placeholder-gray-400"
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <label className="flex items-center mb-4 text-gray-300">
          <input
            type="checkbox"
            checked={remember}
            onChange={e => setRemember(e.target.checked)}
            className="mr-2"
          />
          Remember me
        </label>
        <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded mb-2">Login</button>
        <div className="my-4 border-t border-gray-700"></div>
        <p className="text-gray-400 text-sm">Don't have an account? <Link to="/register" className="text-blue-400">Register</Link></p>
      </form>
    </div>
  );
}

export default Login;