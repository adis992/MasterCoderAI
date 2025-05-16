import React from 'react';
import { useContext } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import './App.css';
import ChatLayout from './components/ChatLayout';
import Login from './components/Login';
import Register from './components/Register';
import { AuthContext } from './context/AuthContext';
import AdminPanel from './components/AdminPanel';

function App() {
  const { user } = useContext(AuthContext);
  const location = useLocation();

  // Automatski redirect root-a na osnovu user role
  if (location.pathname === '/') {
    if (!user) return <Navigate to="/login" />;
    if (user.is_admin) return <Navigate to="/admin" />;
    return <Navigate to="/chat" />;
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/chat" element={user ? <ChatLayout /> : <Navigate to="/login" />} />
        <Route path="/admin" element={user?.is_admin ? <AdminPanel /> : <Navigate to="/chat" />} />
        {/* Root path handled by manual redirect above */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}

export default App;
