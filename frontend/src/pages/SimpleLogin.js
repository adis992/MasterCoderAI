import React, { useState } from 'react';

export default function SimpleLogin({ onLogin, apiUrl }) {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('Testing login...');
    
    try {
      const response = await fetch(`${apiUrl}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
      });
      
      if (response.ok) {
        const data = await response.json();
        setMessage('Login successful!');
        onLogin(data.access_token);
      } else {
        const error = await response.json();
        setMessage(`Login failed: ${error.detail}`);
      }
    } catch (err) {
      setMessage(`Network error: ${err.message}`);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        background: 'rgba(255,255,255,0.1)',
        backdropFilter: 'blur(10px)',
        padding: '2rem',
        borderRadius: '1rem',
        border: '1px solid rgba(255,255,255,0.2)',
        color: 'white',
        minWidth: '300px'
      }}>
        <h1 style={{ textAlign: 'center', marginBottom: '2rem', fontSize: '2rem' }}>
          MasterCoderAI
        </h1>
        
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.5rem',
                border: 'none',
                background: 'rgba(255,255,255,0.2)',
                color: 'white'
              }}
              required
            />
          </div>
          
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '0.5rem',
                border: 'none',
                background: 'rgba(255,255,255,0.2)',
                color: 'white'
              }}
              required
            />
          </div>
          
          <button
            type="submit"
            style={{
              width: '100%',
              padding: '0.75rem',
              borderRadius: '0.5rem',
              border: 'none',
              background: 'white',
              color: '#667eea',
              fontWeight: 'bold',
              cursor: 'pointer',
              marginBottom: '1rem'
            }}
          >
            Login
          </button>
        </form>
        
        {message && (
          <div style={{
            padding: '0.5rem',
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '0.5rem',
            textAlign: 'center',
            fontSize: '0.9rem'
          }}>
            {message}
          </div>
        )}
        
        <div style={{
          textAlign: 'center',
          fontSize: '0.8rem',
          marginTop: '1rem',
          opacity: '0.7'
        }}>
          Default: admin / admin123
        </div>
      </div>
    </div>
  );
}