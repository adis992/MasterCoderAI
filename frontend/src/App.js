import React, { useState, useEffect, useCallback, useRef } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

// Auto-detect API URL based on current hostname
const getApiUrl = () => {
  const hostname = window.location.hostname;
  // If localhost, use localhost. Otherwise use the actual hostname/IP
  return `http://${hostname}:8000`;
};

const API_URL = process.env.REACT_APP_API_URL || getApiUrl();
const INACTIVITY_LIMIT = 30 * 60 * 1000; // 30 minutes

console.log('API_URL:', API_URL); // Debug log

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const inactivityTimeoutRef = useRef(null);

  useEffect(() => {
    if (token) {
      // Decode JWT token (basic)
      try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const payload = JSON.parse(window.atob(base64));
        setUser(payload);
      } catch (e) {
        setToken(null);
        localStorage.removeItem('token');
      }
    }
  }, [token]);

  const login = (newToken) => {
    // Prvo OČISTI sve stare podatke
    localStorage.clear();
    // Onda spremi NOVI token
    localStorage.setItem('token', newToken);
    setToken(newToken);
    console.log('✅ NEW TOKEN SAVED:', newToken.substring(0, 30) + '...');
  };

  const logout = useCallback(() => {
    // HARD CLEAR - obriši SVE iz localStorage
    localStorage.clear();
    setToken(null);
    setUser(null);
    if (inactivityTimeoutRef.current) {
      clearTimeout(inactivityTimeoutRef.current);
    }
    // Force reload da se sve resetuje
    setTimeout(() => {
      window.location.href = '/login';
    }, 100);
  }, []);

  // Auto-logout after 30 minutes of inactivity
  const resetInactivityTimer = useCallback(() => {
    if (inactivityTimeoutRef.current) {
      clearTimeout(inactivityTimeoutRef.current);
    }
    
    if (token) {
      inactivityTimeoutRef.current = setTimeout(() => {
        alert('⏰ Session expired due to inactivity (30 minutes)');
        logout();
      }, INACTIVITY_LIMIT);
    }
  }, [token, logout]);

  useEffect(() => {
    if (!token) return;

    const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'mousemove'];
    
    events.forEach(event => {
      window.addEventListener(event, resetInactivityTimer);
    });

    resetInactivityTimer();

    return () => {
      events.forEach(event => {
        window.removeEventListener(event, resetInactivityTimer);
      });
      if (inactivityTimeoutRef.current) {
        clearTimeout(inactivityTimeoutRef.current);
      }
    };
  }, [token, resetInactivityTimer]);

  return (
    <BrowserRouter>
      <Routes>
        <Route 
          path="/login" 
          element={token ? <Navigate to="/" /> : <Login onLogin={login} apiUrl={API_URL} />} 
        />
        <Route 
          path="/" 
          element={token ? <Dashboard user={user} onLogout={logout} apiUrl={API_URL} /> : <Navigate to="/login" />} 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
