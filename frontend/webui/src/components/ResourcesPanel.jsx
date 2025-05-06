import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';
ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

function ResourcesPanel() {
  const [resources, setResources] = useState(null);
  const [settings, setSettings] = useState({ cpu_enabled: true, gpu_enabled: [] });
  const [gpuSelection, setGpuSelection] = useState([]);

  useEffect(() => {
    axios.get('/admin/resources').then(res => {
      setResources(res.data);
    });
    axios.get('/admin/settings').then(res => {
      setSettings(res.data);
      // handle gpu_enabled as array or boolean
      const gsel = Array.isArray(res.data.gpu_enabled) ? res.data.gpu_enabled : [];
      setGpuSelection(gsel);
    });
  }, []);

  const toggleGpu = (id) => {
    setGpuSelection(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  const saveSettings = () => {
    axios.post('/admin/settings', { cpu_enabled: settings.cpu_enabled, gpu_enabled: gpuSelection })
      .then(res => setSettings(res.data))
      .catch(console.error);
  };

  if (!resources) return <p>Loading...</p>;
  const { cpu_count, cpu_percent, ram_total, ram_used, ram_percent, gpus } = resources;

  const ramData = {
    labels: ['Used', 'Free'],
    datasets: [{ data: [ram_used, ram_total - ram_used], backgroundColor: ['#36A2EB', '#DDD'] }]
  };
  const cpuData = {
    labels: ['Used', 'Free'],
    datasets: [{ data: [cpu_percent, 100 - cpu_percent], backgroundColor: ['#FF6384', '#DDD'] }]
  };
  const gpuData = {
    labels: gpus.map(g => g.name),
    datasets: [{ label: 'GPU Load %', data: gpus.map(g => g.load.toFixed(1)), backgroundColor: '#4BC0C0' }]
  };

  return (
    <div className="text-white p-4">
      <h2 className="text-2xl mb-4">Resources</h2>
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-800 p-4 rounded">
          <h3 className="mb-2">CPU (cores: {cpu_count})</h3>
          <Doughnut data={cpuData} />
        </div>
        <div className="bg-gray-800 p-4 rounded">
          <h3 className="mb-2">RAM</h3>
          <Doughnut data={ramData} />
        </div>
        <div className="col-span-2 bg-gray-800 p-4 rounded">
          <h3 className="mb-2">GPU Load</h3>
          <Bar data={gpuData} />
        </div>
      </div>
      <div className="bg-gray-800 p-4 rounded mb-4">
        <h3 className="mb-2">Enable Resources</h3>
        <label className="mr-4">
          <input type="checkbox" checked={settings.cpu_enabled} onChange={() => setSettings(s => ({ ...s, cpu_enabled: !s.cpu_enabled }))} /> CPU
        </label>
        {gpus.map(g => (
          <label key={g.id} className="mr-4">
            <input type="checkbox" checked={gpuSelection.includes(g.id)} onChange={() => toggleGpu(g.id)} /> GPU {g.id}
          </label>
        ))}
      </div>
      <button onClick={saveSettings} className="px-4 py-2 bg-blue-600 rounded">Save Settings</button>
    </div>
  );
}

export default ResourcesPanel;