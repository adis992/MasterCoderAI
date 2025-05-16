import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';
import { AuthContext } from '../context/AuthContext';
ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

function ResourcesPanel() {
  const { token } = useContext(AuthContext);
  const [resources, setResources] = useState(null);
  const [settings, setSettings] = useState({ cpu_enabled: true, gpu_enabled: [] });
  const [gpuSelection, setGpuSelection] = useState([]);
  const [error, setError] = useState("");
  const [localModel, setLocalModel] = useState(null);
  const [modelStatus, setModelStatus] = useState(null);
  const [models, setModels] = useState([]);
  const [activeModel, setActiveModel] = useState(null);
  const [systemInfo, setSystemInfo] = useState(null);

  // Helper: handle 401 errors globally for this panel
  const handleAxiosError = (err) => {
    if (err.response && err.response.status === 401) {
      setError('Sesija istekla ili nemaš pristup. (401)');
      return;
    } else {
      setError('Greška pri dohvaćanju podataka.');
    }
  };

  useEffect(() => {
    if (!token) {
      setError('Nemaš validan token. Prijavi se ponovo.');
      return;
    }
    axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/resources`, { headers: { Authorization: `Bearer ${token}` } })
      .then(res => {
        setResources(res.data.data);
        setError("");
      }).catch(handleAxiosError);
    axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/settings`, { headers: { Authorization: `Bearer ${token}` } })
      .then(res => {
        setSettings(res.data.data);
        const gsel = Array.isArray(res.data.data.gpu_enabled) ? res.data.data.gpu_enabled : [];
        setGpuSelection(gsel);
      }).catch(handleAxiosError);
    axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/models`, { headers: { Authorization: `Bearer ${token}` } })
      .then(res => {
        setModels(res.data.models || []);
        setActiveModel(res.data.active_model || null);
      }).catch(handleAxiosError);
    axios.get(`${process.env.REACT_APP_API_URL || ''}/system-info`)
      .then(res => {
        setSystemInfo(res.data);
        setError("");
      })
      .catch(() => setSystemInfo(null));
  }, [token]);

  const toggleCpu = () => {
    setSettings(s => ({ ...s, cpu_enabled: !s.cpu_enabled }));
  };
  const toggleGpu = (id) => {
    setGpuSelection(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };
  const saveSettings = () => {
    axios.post(`${process.env.REACT_APP_API_URL || ''}/admin/settings`, { cpu_enabled: settings.cpu_enabled, gpu_enabled: gpuSelection }, { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setSettings(res.data.data))
      .catch(handleAxiosError);
  };
  const handleLocalModel = (e) => {
    const file = e.target.files[0];
    if (file) setLocalModel(file);
  };
  const handleModelLoad = async () => {
    if (!localModel) return;
    setModelStatus('Učitavanje...');
    const formData = new FormData();
    formData.append('file', localModel);
    try {
      await axios.post(`${process.env.REACT_APP_API_URL || ''}/admin/upload_model`, formData, {
        headers: { 'Content-Type': 'multipart/form-data', Authorization: `Bearer ${token}` }
      });
      await axios.post(`${process.env.REACT_APP_API_URL || ''}/admin/load_model`, { model_name: localModel.name }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setModelStatus('Model uspješno uploadovan i učitan: ' + localModel.name);
      const res = await axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/models`, { headers: { Authorization: `Bearer ${token}` } });
      setModels(res.data.models || []);
      setActiveModel(res.data.active_model || null);
    } catch (err) {
      setModelStatus('Greška pri uploadu ili učitavanju modela!');
      handleAxiosError(err);
    }
  };

  if (error) return <div className="text-red-400 bg-gray-900 rounded text-center">{error}</div>;
  if (!resources) return <p>Učitavanje...</p>;
  const { cpu_count, cpu_percent, ram_total, ram_used, gpus } = resources;

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
    <div className="w-full max-w-3xl mx-auto p-8 py-8 bg-gray-900 rounded-2xl shadow-2xl border border-blue-900">
      <div className="text-white w-full max-w-5xl p-4">
        <h2 className="text-2xl mb-2 sm:mb-4">Resursi</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mb-6 auto-rows-fr">
          <div className="bg-gray-800 rounded min-h-[280px] h-72 flex flex-col justify-center p-4">
            <h3 className="mb-2">CPU (jezgre: {cpu_count})</h3>
            <Doughnut data={cpuData} options={{ maintainAspectRatio: false, responsive: true }} height={220} />
          </div>
          <div className="bg-gray-800 rounded min-h-[280px] h-72 flex flex-col justify-center p-4">
            <h3 className="mb-2">RAM</h3>
            <Doughnut data={ramData} options={{ maintainAspectRatio: false, responsive: true }} height={220} />
          </div>
          <div className="bg-gray-800 rounded min-h-[280px] h-72 flex flex-col justify-center p-4">
            <h3 className="mb-2">GPU opterećenje</h3>
            <Bar data={gpuData} options={{ maintainAspectRatio: false, responsive: true }} height={220} />
          </div>
        </div>
        <div className="bg-gray-800 rounded mb-2 sm:mb-4 p-4">
          <h3 className="mb-2">Omogući resurse za AI model</h3>
          <label className="mr-4 font-semibold">
            <input type="checkbox" checked={settings.cpu_enabled} onChange={toggleCpu} /> CPU
          </label>
          {resources && resources.gpus && resources.gpus.length > 0 ? resources.gpus.map(g => (
            <label key={g.id} className="mr-4 font-semibold">
              <input type="checkbox" checked={gpuSelection.includes(g.id)} onChange={() => toggleGpu(g.id)} /> GPU {g.id} <span className="text-xs text-blue-300">({g.name})</span>
            </label>
          )) : <span className="italic text-blue-400">Nema GPU uređaja</span>}
          <span className="ml-4 text-blue-200 font-bold">Ukupni VRAM: {resources ? resources.gpus.reduce((acc, g) => acc + (g.memory_total || 0), 0) : 0} MB</span>
          <button onClick={saveSettings} className="ml-4 px-4 py-2 bg-blue-600 rounded">Spremi</button>
        </div>
        <div className="bg-gray-800 rounded mb-2 sm:mb-4 flex flex-col sm:flex-row items-center gap-4 p-4">
          <label className="font-semibold">Učitaj lokalni AI model:</label>
          <input type="file" accept=".bin,.pt,.gguf,.onnx,.pkl,.ckpt,.safetensors,.zip" onChange={handleLocalModel} className="bg-gray-900 rounded" />
          {localModel && <span className="text-blue-300 text-sm">{localModel.name}</span>}
          <button className="px-4 py-2 bg-blue-700 rounded text-white" onClick={handleModelLoad} disabled={!localModel}>Uploadaj model</button>
          {modelStatus && <span className="ml-2 text-green-400 font-semibold">{modelStatus}</span>}
        </div>
        <div className="bg-gray-800 rounded mb-2 sm:mb-4 p-4">
          <h3 className="mb-2">Status modela</h3>
          {activeModel ? (
            <span className="text-green-400 font-bold">Učitani model: {activeModel}</span>
          ) : (
            <span className="text-red-400">Nijedan model nije učitan.</span>
          )}
          <div className="mt-2 text-blue-200 text-sm">Dostupni modeli: {models.length ? models.join(', ') : 'nema'}</div>
        </div>
        <div>
          <h2 className="text-xl font-bold mb-4">System Information</h2>
          {error && <p className="text-red-500">{error}</p>}
          {systemInfo ? (
            <div>
              <h3 className="text-lg font-semibold">CPU</h3>
              <p>Logical Cores: {systemInfo.cpu.logical_cores}</p>
              <p>Physical Cores: {systemInfo.cpu.physical_cores}</p>

              <h3 className="text-lg font-semibold mt-4">GPUs</h3>
              {systemInfo.gpus.map(gpu => (
                <div key={gpu.id} className="mb-2">
                  <p>Name: {gpu.name}</p>
                  <p>Total Memory: {gpu.total_memory} MB</p>
                  <p>Available Memory: {gpu.available_memory} MB</p>
                  <button
                    onClick={() => toggleGpu(gpu.id)}
                    className={`px-4 py-2 mt-2 rounded ${gpuSelection.includes(gpu.id) ? 'bg-red-500' : 'bg-green-500'}`}
                  >
                    {gpuSelection.includes(gpu.id) ? 'Disable' : 'Enable'} GPU
                  </button>
                </div>
              ))}

              <h3 className="text-lg font-semibold mt-4">Total VRAM</h3>
              <p>{systemInfo.total_vram} MB</p>
            </div>
          ) : (
            <p>Loading system information...</p>
          )}

          <button
            onClick={saveSettings}
            className="px-4 py-2 mt-4 bg-blue-500 text-white rounded"
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
}

export default ResourcesPanel;