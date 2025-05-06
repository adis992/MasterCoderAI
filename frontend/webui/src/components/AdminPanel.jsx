import React, { useState } from 'react';
import UsersList from './UsersList';
import TasksList from './TasksList';
import ResourcesPanel from './ResourcesPanel';
import AdminSettingsPanel from './AdminSettingsPanel';

function AdminPanel() {
  const [tab, setTab] = useState('users');
  return (
    <div className="min-h-screen bg-gray-900 p-8 text-white">
      <h1 className="text-3xl mb-4">Admin Dashboard</h1>
      <nav className="flex space-x-4 border-b border-gray-700 pb-2">
        <button onClick={() => setTab('users')} className={`px-4 py-2 ${tab==='users'?'border-b-2 border-blue-400':''}`}>Users</button>
        <button onClick={() => setTab('tasks')} className={`px-4 py-2 ${tab==='tasks'?'border-b-2 border-blue-400':''}`}>Tasks</button>
        <button onClick={() => setTab('resources')} className={`px-4 py-2 ${tab==='resources'?'border-b-2 border-blue-400':''}`}>Resources</button>
        <button onClick={() => setTab('settings')} className={`px-4 py-2 ${tab==='settings'?'border-b-2 border-blue-400':''}`}>Settings</button>
      </nav>
      <div className="mt-6">
        {tab === 'users' && <UsersList />}
        {tab === 'tasks' && <TasksList />}
        {tab === 'resources' && <ResourcesPanel />}
        {tab === 'settings' && <AdminSettingsPanel />}
      </div>
    </div>
  );
}

export default AdminPanel;