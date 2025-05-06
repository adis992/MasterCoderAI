import React from 'react';
import { useContext } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import ChatLayout from './components/ChatLayout';
import Login from './components/Login';
import Register from './components/Register';
import { AuthContext } from './context/AuthContext';
import AdminPanel from './components/AdminPanel';

function App() {
  const { user } = useContext(AuthContext);
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={user ? <ChatLayout /> : <Navigate to="/login" />} />
        <Route path="/admin" element={
          user?.is_admin ? <AdminPanel /> : <Navigate to="/" />
        } />
        <Route path="*" element={<Navigate to={user ? "/" : "/login"} />} />
      </Routes>
    </div>
  );
}

export default App;
