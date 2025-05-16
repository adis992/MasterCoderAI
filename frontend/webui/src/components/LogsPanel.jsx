import React, { useState, useEffect } from 'react';
import axios from 'axios';

function LogsPanel() {
  const [logs, setLogs] = useState({ general: '', chat: '', model: '', settings: '' });
  const [loading, setLoading] = useState(true);
  const API_URL = process.env.REACT_APP_API_URL || '';

  useEffect(() => {
    async function fetchLogs() {
      setLoading(true);
      try {
        // Fetch all log categories from backend; ensure your API provides these endpoints
        const res = await axios.get(`${API_URL}/admin/logs`);
        setLogs(res.data);
      } catch (error) {
        console.error('Failed to load logs:', error);
      }
      setLoading(false);
    }
    fetchLogs();
  }, [API_URL]);

  if (loading) {
    return <div className="p-4 text-white">Loading logs...</div>;
  }

  return (
    <div className="p-4 space-y-6 text-white text-left overflow-auto">
      <section>
        <h2 className="text-xl font-bold mb-2">General Logs</h2>
        <pre className="bg-gray-800 p-3 rounded-lg max-h-40 overflow-auto">{logs.general}</pre>
      </section>
      <section>
        <h2 className="text-xl font-bold mb-2">Chat Errors</h2>
        <pre className="bg-gray-800 p-3 rounded-lg max-h-40 overflow-auto">{logs.chat}</pre>
      </section>
      <section>
        <h2 className="text-xl font-bold mb-2">Model Logs</h2>
        <pre className="bg-gray-800 p-3 rounded-lg max-h-40 overflow-auto">{logs.model}</pre>
      </section>
      <section>
        <h2 className="text-xl font-bold mb-2">Settings Logs</h2>
        <pre className="bg-gray-800 p-3 rounded-lg max-h-40 overflow-auto">{logs.settings}</pre>
      </section>
    </div>
  );
}

export default LogsPanel;
