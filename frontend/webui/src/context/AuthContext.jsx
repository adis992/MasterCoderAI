import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import axios from 'axios';

export const AuthContext = createContext();

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'; // fallback for local dev

function getInitialToken() {
  // Prefer sessionStorage, fallback to localStorage
  return sessionStorage.getItem('token') || localStorage.getItem('token') || null;
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(getInitialToken());
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      // Set token in axios and decode user
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      const decoded = jwtDecode(token);
      setUser(decoded);
      console.log('AuthContext user:', decoded); // DEBUG
      // Save token to correct storage
      if (sessionStorage.getItem('token') === token) {
        // Session-only
        localStorage.removeItem('token');
      } else {
        // Persistent
        localStorage.setItem('token', token);
        sessionStorage.removeItem('token');
      }
    } else {
      delete axios.defaults.headers.common['Authorization'];
      localStorage.removeItem('token');
      sessionStorage.removeItem('token');
      setUser(null);
    }
  }, [token]);

  // Remove forced logout on browser close for persistent login

  const login = async (username, password, remember = false) => {
    const res = await axios.post(`${API_URL}/auth/login`, { username, password });
    if (remember) {
      localStorage.setItem('token', res.data.access_token);
      sessionStorage.removeItem('token');
    } else {
      sessionStorage.setItem('token', res.data.access_token);
      localStorage.removeItem('token');
    }
    setToken(res.data.access_token);
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem('token');
    sessionStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
