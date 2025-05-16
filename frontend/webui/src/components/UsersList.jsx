import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UsersList() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [newUser, setNewUser] = useState({ username: '', password: '', is_admin: false });
  const [creating, setCreating] = useState(false);
  const [editId, setEditId] = useState(null);
  const [editRole, setEditRole] = useState({});

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/users`)
      .then(res => setUsers(res.data.data || []))
      .catch(err => setError('Greška pri dohvaćanju korisnika.'));
  }, []);

  const handleDelete = (id, username) => {
    if (id === 1 || username === 'admin') return; // Prevent deleting main admin
    axios.delete(`${process.env.REACT_APP_API_URL || ''}/admin/users/${id}`)
      .then(() => setUsers(prev => prev.filter(u => u.id !== id)))
      .catch(() => setError('Greška pri brisanju korisnika.'));
  };

  const handleCreate = (e) => {
    e.preventDefault();
    setCreating(true);
    axios.post(`${process.env.REACT_APP_API_URL || ''}/auth/register`, newUser)
      .then(res => {
        setUsers(prev => [...prev, { id: res.data.id, username: newUser.username, is_admin: newUser.is_admin }]);
        setNewUser({ username: '', password: '', is_admin: false });
        setError("");
      })
      .catch(() => setError('Greška pri kreiranju korisnika.'))
      .finally(() => setCreating(false));
  };

  const handleEdit = (id, is_admin) => {
    setEditId(id);
    setEditRole({ is_admin });
  };

  const handleRoleChange = (id, role) => {
    setEditRole(prev => ({ ...prev, [role]: !prev[role] }));
  };

  const handleSave = (id, username) => {
    if (id === 1 || username === 'admin') return; // Prevent editing main admin
    axios.patch(`${process.env.REACT_APP_API_URL || ''}/admin/users/${id}`, { is_admin: !!editRole.is_admin })
      .then(() => {
        setUsers(prev => prev.map(u => u.id === id ? { ...u, is_admin: !!editRole.is_admin } : u));
        setEditId(null);
        setEditRole({});
      })
      .catch(() => setError('Greška pri spremanju uloge.'));
  };

  return (
    <div className="py-8">
      <div className="w-full max-w-4xl mx-auto p-6 bg-gray-900 rounded-xl shadow-xl border border-gray-800">
        <h2 className="text-3xl font-bold mb-6 text-gray-100 tracking-tight flex items-center gap-2">
          <span className="inline-block bg-gradient-to-r from-green-400 to-blue-500 text-transparent bg-clip-text">Users</span>
          <span className="ml-2 text-base font-normal text-gray-400">Admin Management</span>
        </h2>
        {error && <div className="text-red-400 mb-4 font-semibold bg-red-900/40 rounded p-2 border border-red-700 animate-pulse">{error}</div>}
        <form className="bg-gray-800 rounded-lg p-6 mb-8 shadow flex flex-col md:flex-row gap-4 items-end border border-gray-700" onSubmit={handleCreate}>
          <div className="flex-1 flex flex-col gap-2">
            <input className="p-2 rounded bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Username" value={newUser.username} onChange={e => setNewUser({ ...newUser, username: e.target.value })} required />
            <input className="p-2 rounded bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Password" type="password" value={newUser.password} onChange={e => setNewUser({ ...newUser, password: e.target.value })} required />
          </div>
          <label className="flex items-center text-gray-300 mb-2 md:mb-0">
            <input type="checkbox" checked={newUser.is_admin} onChange={e => setNewUser({ ...newUser, is_admin: e.target.checked })} className="mr-2 accent-green-500" />Admin
          </label>
          <button className="bg-gradient-to-r from-green-500 to-blue-600 px-6 py-2 rounded text-white font-semibold shadow hover:from-green-400 hover:to-blue-500 transition disabled:opacity-60" disabled={creating}>Create</button>
        </form>
        <div className="overflow-x-auto rounded-lg shadow border border-gray-700">
          <table className="min-w-full bg-gray-900 rounded-lg">
            <thead>
              <tr className="bg-gray-800 text-gray-200 text-lg">
                <th className="px-4 py-3 font-semibold">ID</th>
                <th className="px-4 py-3 font-semibold">Username</th>
                <th className="px-4 py-3 font-semibold">Admin</th>
                <th className="px-4 py-3 font-semibold">User</th>
                <th className="px-4 py-3 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.length === 0 ? (
                <tr><td colSpan={5} className="text-center py-10 text-gray-500 text-xl">No users found.</td></tr>
              ) : users.map((u, idx) => (
                <tr key={u.id} className={idx % 2 === 0 ? 'bg-gray-950' : 'bg-gray-900 hover:bg-gray-800/80 transition'}>
                  <td className="border-t border-gray-800 px-4 py-3 text-center">{u.id}</td>
                  <td className="border-t border-gray-800 px-4 py-3 font-mono text-green-300 text-center">{u.username}</td>
                  <td className="border-t border-gray-800 px-4 py-3 text-center">
                    <input type="checkbox" checked={editId === u.id ? !!editRole.is_admin : !!u.is_admin} disabled={u.id === 1 || u.username === 'admin'} onChange={() => handleRoleChange(u.id, 'is_admin')} className="accent-green-500 scale-125" />
                  </td>
                  <td className="border-t border-gray-800 px-4 py-3 text-center">
                    <input type="checkbox" checked={editId === u.id ? !editRole.is_admin : !u.is_admin} disabled={true} readOnly className="accent-blue-500 scale-125 opacity-60" />
                  </td>
                  <td className="border-t border-gray-800 px-4 py-3 flex gap-2 justify-center">
                    {u.id !== 1 && u.username !== 'admin' && (
                      editId === u.id ? (
                        <button className="bg-blue-600 px-3 py-1 rounded text-white font-semibold shadow hover:bg-blue-500 transition" onClick={() => handleSave(u.id, u.username)}>Save</button>
                      ) : (
                        <button className="bg-gray-700 px-3 py-1 rounded text-white font-semibold shadow hover:bg-gray-600 transition" onClick={() => handleEdit(u.id, u.is_admin)}>Edit</button>
                      )
                    )}
                    {u.id !== 1 && u.username !== 'admin' && (
                      <button onClick={() => handleDelete(u.id, u.username)} className="px-3 py-1 bg-red-600 rounded text-white font-semibold shadow hover:bg-red-500 transition">Delete</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default UsersList;