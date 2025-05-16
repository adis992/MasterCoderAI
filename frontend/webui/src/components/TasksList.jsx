import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TasksList() {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/tasks`)
      .then(res => setTasks(res.data.data || []))
      .catch(() => setError('Greška pri dohvaćanju zadataka.'));
  }, []);

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-gray-900 rounded-xl shadow-xl border border-gray-800">
      <h2 className="text-3xl font-bold mb-6 text-gray-100 tracking-tight flex items-center gap-2">
        <span className="inline-block bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">Tasks</span>
        <span className="ml-2 text-base font-normal text-gray-400">System Jobs</span>
      </h2>
      {error && <div className="text-red-400 mb-4 font-semibold bg-red-900/40 rounded p-2 border border-red-700 animate-pulse">{error}</div>}
      <div className="overflow-x-auto rounded-lg shadow border border-gray-700">
        <table className="min-w-full bg-gray-900 rounded-lg">
          <thead>
            <tr className="bg-gray-800 text-gray-200 text-lg">
              <th className="px-4 py-3 font-semibold">ID</th>
              <th className="px-4 py-3 font-semibold">Type</th>
              <th className="px-4 py-3 font-semibold">Status</th>
              <th className="px-4 py-3 font-semibold">User</th>
              <th className="px-4 py-3 font-semibold">Created</th>
              <th className="px-4 py-3 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {tasks.length === 0 ? (
              <tr><td colSpan={6} className="text-center py-10 text-gray-500 text-xl">No tasks found.</td></tr>
            ) : tasks.map((t, idx) => (
              <tr key={t.id} className={idx % 2 === 0 ? 'bg-gray-950' : 'bg-gray-900 hover:bg-gray-800/80 transition'}>
                <td className="border-t border-gray-800 px-4 py-3 text-center">{t.id}</td>
                <td className="border-t border-gray-800 px-4 py-3 text-center font-mono text-blue-300">{t.type}</td>
                <td className="border-t border-gray-800 px-4 py-3 text-center">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${t.status === 'completed' ? 'bg-green-700 text-green-200' : t.status === 'failed' ? 'bg-red-700 text-red-200' : 'bg-blue-700 text-blue-200'}`}>{t.status}</span>
                </td>
                <td className="border-t border-gray-800 px-4 py-3 text-center text-purple-300">{t.user}</td>
                <td className="border-t border-gray-800 px-4 py-3 text-center text-gray-400">{t.created_at}</td>
                <td className="border-t border-gray-800 px-4 py-3 flex gap-2 justify-center">
                  {/* Add task actions here if needed */}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default TasksList;