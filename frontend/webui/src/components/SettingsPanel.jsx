import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function SettingsPanel() {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  if (user?.is_admin) {
    // Automatski redirect admina na AdminSettingsPanel
    navigate('/admin', { replace: true });
    return null;
  }

  // User settings (stub ili osnovne postavke)
  return (
    <aside className="settings-panel w-full">
      <h2 className="text-lg font-bold mb-4">Settings</h2>
      <div className="mb-4 text-blue-300">Sistemske postavke su dostupne samo adminu.</div>
    </aside>
  );
}

export default SettingsPanel;