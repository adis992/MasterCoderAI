import React, { useState } from 'react';
import ChatLayout from './ChatLayout';
import UsersList from './UsersList';
import TasksList from './TasksList';
import ResourcesPanel from './ResourcesPanel';
import AdminSettingsPanel from './AdminSettingsPanel';
import LogsPanel from './LogsPanel';
import AnalyticsPanel from './AnalyticsPanel';
import ApiPanel from './ApiPanel';
import { AuthContext } from '../context/AuthContext';

const tabs = [
  { key: 'chat', label: 'Chat' },
  { key: 'users', label: 'Users' },
  { key: 'tasks', label: 'Tasks' },
  { key: 'resources', label: 'Resources' },
  { key: 'logs', label: 'Logs' },
  { key: 'analytics', label: 'Analytics' },
  { key: 'api', label: 'API' },
  { key: 'settings', label: 'Settings' },
];

function AdminPanel() {
  const { logout, user } = React.useContext(AuthContext);
  const [tab, setTab] = useState('chat');

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 text-white flex flex-col">
      <nav className="w-full flex gap-2 bg-gray-800 border-b border-blue-900 px-4 py-3 sticky top-0 z-30 relative items-center shadow-lg rounded-b-xl">
        <h1 className="font-bold text-blue-400 text-2xl tracking-wide mr-8 drop-shadow">MasterCoderAI</h1>
        {tabs.map(t => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors shadow-sm border ${tab===t.key
              ? 'bg-blue-600 text-white border-blue-300'
              : 'bg-gray-800 text-gray-300 hover:bg-gray-700 border-transparent'} `}
          >{t.label}</button>
        ))}
        <div className="flex-1"></div>
        {user && user.is_admin && (
          <button
            onClick={logout}
            className="ml-auto px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg font-semibold shadow-md transition-colors"
          >Logout</button>
        )}
      </nav>
      <main className="flex-1 flex flex-col items-start justify-start py-8">
        <div className={`w-full ${tab==='chat' ? '' : 'max-w-6xl mx-auto'}`}>
          {tab === 'chat' && <ChatLayout />}
          {tab === 'users' && <UsersList />}
          {tab === 'tasks' && <TasksList />}
          {tab === 'resources' && <ResourcesPanel />}
          {tab === 'logs' && <LogsPanel />}
          {tab === 'analytics' && <AnalyticsPanel />}
          {tab === 'api' && <ApiPanel />}
          {tab === 'settings' && <AdminSettingsPanel />}
        </div>
      </main>
    </div>
  );
}

export default AdminPanel;