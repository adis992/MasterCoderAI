import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AdminSettingsPanel() {
  const [settings, setSettings] = useState({ cpu_enabled: true, gpu_enabled: [] });
  const [gpuSelection, setGpuSelection] = useState([]);

  useEffect(() => {
    axios.get('/admin/settings')
      .then(res => {
        setSettings(res.data);
        setGpuSelection(Array.isArray(res.data.gpu_enabled) ? res.data.gpu_enabled : []);
      })
      .catch(console.error);
  }, []);

  const toggleGpu = id => {
    setGpuSelection(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  const save = () => {
    axios.post('/admin/settings', { cpu_enabled: settings.cpu_enabled, gpu_enabled: gpuSelection })
      .then(res => setSettings(res.data))
      .catch(console.error);
  };

  return (
    <div className="text-white p-4">
      <h2 className="text-2xl mb-4">Settings</h2>
      <div className="bg-gray-800 p-4 rounded mb-4">
        <label className="flex items-center mb-2">
          <input
            type="checkbox"
            checked={settings.cpu_enabled}
            onChange={() => setSettings(s => ({ ...s, cpu_enabled: !s.cpu_enabled }))}
            className="mr-2"
          />
          Enable CPU Tasks
        </label>
        <div className="mb-2">Enable GPU Tasks:</div>
        {settings.gpu_enabled !== undefined && gpuSelection.map(id => id).length >= 0 && (
          <div className="flex flex-wrap gap-4">
            {gpuSelection.map((id) => (
              <label key={id} className="flex items-center">
                <input
                  type="checkbox"
                  checked={gpuSelection.includes(id)}
                  onChange={() => toggleGpu(id)}
                  className="mr-2"
                />
                GPU {id}
              </label>
            ))}
          </div>
        )}
      </div>
      <button onClick={save} className="px-4 py-2 bg-blue-600 rounded">Save Settings</button>
    </div>
  );
}

export default AdminSettingsPanel;