// filepath: src/components/ApiPanel.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ApiPanel() {
  const [endpoints, setEndpoints] = useState([]);
  const API_URL = process.env.REACT_APP_API_URL || '';

  useEffect(() => {
    axios.get(`${API_URL}/admin/api-spec`)
      .then(res => {
        const base = res.data.endpoints || [];
        const extra = [
          { method: 'GET', path: '/admin/logs', description: 'Fetch system and chat logs' },
          { method: 'GET', path: '/admin/analytics', description: 'Fetch analytics metrics' },
          { method: 'GET', path: '/admin/api-spec', description: 'Fetch API specification' },
          { method: 'POST', path: '/chat', description: 'Send a message to the local ChatGPT model' },
          { method: 'GET', path: '/openai/models', description: 'List available OpenAI/ChatGPT models' },
          { method: 'POST', path: '/openai/chat/completions', description: 'OpenAI Chat Completions endpoint' },
          { method: 'POST', path: '/auth/login', description: 'Authenticate user and return a token' },
          { method: 'POST', path: '/auth/register', description: 'Register a new user' },
        ];
        setEndpoints([...base, ...extra]);
      })
      .catch(err => console.error(err));
  }, [API_URL]);

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-xl font-bold mb-4 text-white">API Endpoints</h2>
      <div className="space-y-6">
        {endpoints.map(ep => (
          <div key={ep.path} className="bg-gray-800 p-4 rounded-lg text-white">
            <div><span className="font-semibold">{ep.method}</span> <span className="font-mono">{ep.path}</span></div>
            <p className="mt-1 text-gray-300">{ep.description}</p>
            {ep.parameters && ep.parameters.length > 0 && (
              <div className="mt-2">
                <h3 className="font-semibold">Parameters:</h3>
                <ul className="list-disc list-inside text-gray-300">
                  {ep.parameters.map(param => <li key={param.name}>{param.name} ({param.in}): {param.description}</li>)}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ApiPanel;
