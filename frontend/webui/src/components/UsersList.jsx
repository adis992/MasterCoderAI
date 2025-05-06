import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UsersList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get('/admin/users')
      .then(res => setUsers(res.data))
      .catch(console.error);
  }, []);

  const handleDelete = (id) => {
    axios.delete(`/admin/users/${id}`)
      .then(() => setUsers(prev => prev.filter(u => u.id !== id)))
      .catch(console.error);
  };

  return (
    <div>
      <h2 className="text-2xl text-white mb-4">Users</h2>
      <table className="min-w-full table-auto bg-gray-800 text-white rounded">
        <thead>
          <tr>
            <th className="px-4 py-2">ID</th>
            <th className="px-4 py-2">Username</th>
            <th className="px-4 py-2">Role</th>
            <th className="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id} className="hover:bg-gray-700">
              <td className="border px-4 py-2">{u.id}</td>
              <td className="border px-4 py-2">{u.username}</td>
              <td className="border px-4 py-2">{u.is_admin ? 'Admin' : 'User'}</td>
              <td className="border px-4 py-2">
                <button onClick={() => handleDelete(u.id)} className="px-2 py-1 bg-red-600 rounded">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UsersList;