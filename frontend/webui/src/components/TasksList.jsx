import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TasksList() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    axios.get('/admin/tasks')
      .then(res => setTasks(res.data))
      .catch(console.error);
  }, []);

  const handleDelete = (id) => {
    axios.delete(`/admin/tasks/${id}`)
      .then(() => setTasks(prev => prev.filter(t => t.id !== id)))
      .catch(console.error);
  };

  return (
    <div>
      <h2 className="text-2xl text-white mb-4">Tasks</h2>
      <table className="min-w-full table-auto bg-gray-800 text-white rounded">
        <thead>
          <tr>
            <th className="px-4 py-2">ID</th>
            <th className="px-4 py-2">User ID</th>
            <th className="px-4 py-2">Status</th>
            <th className="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map(t => (
            <tr key={t.id} className="hover:bg-gray-700">
              <td className="border px-4 py-2">{t.id}</td>
              <td className="border px-4 py-2">{t.user_id}</td>
              <td className="border px-4 py-2">{t.status}</td>
              <td className="border px-4 py-2">
                <button onClick={() => handleDelete(t.id)} className="px-2 py-1 bg-red-600 rounded">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TasksList;