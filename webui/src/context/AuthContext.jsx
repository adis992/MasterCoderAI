import React, { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [role, setRole] = useState(null);

  // On mount, check existing token
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      try {
        const { sub, role: userRole, exp } = jwtDecode(token);
        if (Date.now() < exp * 1000) {
          setUser({ id: sub });
          setRole(userRole);
        } else {
          localStorage.removeItem('auth_token');
        }
      } catch (err) {
        console.error('Invalid token on load:', err);
        localStorage.removeItem('auth_token');
      }
    }
  }, []);

  const login = async () => {
    // Placeholder: redirect to OAuth2 or show JWT prompt
    const token = prompt('Enter JWT token');
    if (token) {
      try {
        const { sub, role: userRole } = jwtDecode(token);
        localStorage.setItem('auth_token', token);
        setUser({ id: sub });
        setRole(userRole);
      } catch (err) {
        console.error('Invalid token entered:', err);
        alert('Invalid JWT token. Please enter a valid token.');
      }
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setUser(null);
    setRole(null);
  };

  return (
    <AuthContext.Provider value={{ user, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
