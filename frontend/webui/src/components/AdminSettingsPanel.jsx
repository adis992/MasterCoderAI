import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';

function AdminSettingsPanel() {
  const { user, token } = useContext(AuthContext);
  const [settings, setSettings] = useState({ cpu_enabled: true, gpu_enabled: [], temperature: 0.7, max_tokens: 1024, active_model: null });
  const [gpuSelection, setGpuSelection] = useState([]);
  const [models, setModels] = useState([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [systemInfo, setSystemInfo] = useState(null);
  const [modelLoadStatus, setModelLoadStatus] = useState("");

  // Helper: handle 401 errors globally for this panel
  const handleAxiosError = (err) => {
    if (err.response && err.response.status === 401) {
      setError('Sesija istekla ili nemaš pristup. (401)');
      return;
    } else {
      setError('Greška pri dohvaćanju podataka.');
    }
  };

  // Always fetch data when token becomes available
  useEffect(() => {
    if (!token) {
      setError('Nemaš validan token. Prijavi se ponovo.');
      setSettings({ cpu_enabled: true, gpu_enabled: [], temperature: 0.7, max_tokens: 1024, active_model: null });
      setGpuSelection([]);
      setModels([]);
      setSystemInfo(null);
      return;
    }
    setError("");
    axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/settings`, { headers: { Authorization: `Bearer ${token}` } })
      .then(res => {
        setSettings(res.data.data);
        setGpuSelection(Array.isArray(res.data.data.gpu_enabled) ? res.data.data.gpu_enabled : []);
      })
      .catch(handleAxiosError);
    axios.get(`${process.env.REACT_APP_API_URL || ''}/system-info`)
      .then(res => setSystemInfo(res.data))
      .catch(() => setSystemInfo(null));
    axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/models`, { headers: { Authorization: `Bearer ${token}` } })
      .then(res => {
        setModels(res.data.models || []);
      })
      .catch(handleAxiosError);
  }, [token]);

  const handleChange = e => {
    const { name, value, checked } = e.target;
    if (name === 'cpu_enabled') setSettings(s => ({ ...s, cpu_enabled: checked }));
    else if (name === 'temperature') setSettings(s => ({ ...s, temperature: parseFloat(value) }));
    else if (name === 'max_tokens') setSettings(s => ({ ...s, max_tokens: parseInt(value) }));
    else if (name === 'active_model') setSettings(s => ({ ...s, active_model: value }));
  };
  const toggleGpu = id => {
    setGpuSelection(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);
  };
  const save = () => {
    if (!settings.active_model) {
      setError('Prvo učitaj model prije promjene GPU/CPU postavki!');
      setSuccess("");
      return;
    }
    setSaving(true);
    setError("");
    setSuccess("");
    axios.post(`${process.env.REACT_APP_API_URL || ''}/admin/settings`, {
      cpu_enabled: settings.cpu_enabled,
      gpu_enabled: gpuSelection,
      temperature: settings.temperature,
      max_tokens: settings.max_tokens,
      active_model: settings.active_model
    }, { headers: { Authorization: `Bearer ${token}` } })
      .then(res => {
        setSettings(res.data.data);
        setSuccess("Postavke spremljene.");
      })
      .catch(err => {
        setError(err.response?.data?.detail ? JSON.stringify(err.response.data.detail) : "Greška pri spremanju postavki.");
      })
      .finally(() => setSaving(false));
  };

  const handleLoadModel = async () => {
    setModelLoadStatus("Učitavanje modela...");
    setError("");
    try {
      await axios.post(
        `${process.env.REACT_APP_API_URL || ''}/admin/load_model`,
        { model_name: settings.active_model },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setModelLoadStatus(`Model '${settings.active_model}' uspješno učitan!`);
      setSuccess("Model uspješno učitan.");
    } catch (err) {
      setModelLoadStatus("");
      setError(err.response?.data?.detail || "Greška pri učitavanju modela.");
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-8 py-8 bg-gray-900 rounded-2xl shadow-2xl border border-blue-900 mt-8 mb-8">
      <h2 className="text-3xl font-bold mb-8 text-blue-200 tracking-tight flex items-center gap-2">
        <span className="inline-block bg-gradient-to-r from-blue-400 to-green-400 text-transparent bg-clip-text">Admin Settings</span>
      </h2>
      <div className="space-y-8">
        <section className="bg-gray-800 rounded-lg p-6 shadow border border-gray-700">
          <h3 className="text-xl font-semibold text-gray-100 mb-4">General Settings</h3>
          <div className="mb-2 text-blue-200 text-sm">Korisnik: <span className="font-bold">{user?.username || 'n/a'}</span> ({user?.is_admin ? 'admin' : 'user'})</div>
          <div className="flex flex-col gap-2 mb-4">
            <label className="flex items-center mb-2 font-semibold text-blue-300">
              <input
                type="checkbox"
                name="cpu_enabled"
                checked={settings.cpu_enabled}
                onChange={handleChange}
                className="mr-2"
              />
              Omogući CPU
            </label>
            <div className="mb-2 font-semibold text-blue-300">Omogući GPU:</div>
            <div className="flex flex-wrap gap-4 mb-2">
              {systemInfo && systemInfo.gpus.length === 0 && <span className="italic text-blue-400">Nema GPU uređaja</span>}
              {systemInfo && systemInfo.gpus.map(gpu => (
                <label key={gpu.id} className="flex items-center text-blue-200">
                  <input
                    type="checkbox"
                    checked={gpuSelection.includes(gpu.id)}
                    onChange={() => toggleGpu(gpu.id)}
                    className="mr-2"
                  />
                  {gpu.name} <span className="ml-1 text-xs text-blue-400">(ID: {gpu.id})</span>
                </label>
              ))}
            </div>
            {systemInfo && (
              <div className="mb-2 text-blue-200">Ukupni VRAM: <span className="font-bold">{systemInfo.total_vram} MB</span></div>
            )}
          </div>
        </section>
        <section className="bg-gray-800 rounded-lg p-6 shadow border border-gray-700">
          <h3 className="text-xl font-semibold text-gray-100 mb-4">Advanced</h3>
          <div className="flex flex-col gap-2 mb-4 p-4 bg-gray-900 rounded">
            <div className="mb-2 font-semibold text-blue-300">Napredne postavke modela:</div>
            <div className="mb-2 font-semibold text-blue-300">Model:</div>
            <select
              name="active_model"
              value={settings.active_model || ''}
              onChange={handleChange}
              className="rounded bg-gray-900 text-blue-100 border border-blue-700 mb-4"
            >
              <option value="">-- Odaberi model --</option>
              {models.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
            <button
              onClick={handleLoadModel}
              className="px-4 py-2 bg-green-600 rounded font-bold text-white mb-2"
              disabled={!settings.active_model}
            >Učitaj model</button>
            {modelLoadStatus && <div className="text-blue-400 mt-2">{modelLoadStatus}</div>}
            <div className="mb-2 font-semibold text-blue-300">Temperature: <span className='text-blue-200 font-bold ml-2'>{settings.temperature}</span></div>
            <input
              type="range"
              name="temperature"
              min="0"
              max="2"
              step="0.01"
              value={settings.temperature}
              onChange={handleChange}
              className="w-full mb-2"
            />
            <div className="mb-2 font-semibold text-blue-300 mt-4">Max tokens:</div>
            <input
              type="number"
              name="max_tokens"
              min="1"
              max="8192"
              value={settings.max_tokens}
              onChange={handleChange}
              className="rounded bg-gray-900 text-blue-100 border border-blue-700 mb-2"
            />
          </div>
        </section>
      </div>
      <button onClick={save} className="px-4 py-2 bg-blue-600 rounded font-bold text-white mt-4" disabled={saving || !settings.active_model}>
        {saving ? 'Spremanje...' : 'Spremi postavke'}
      </button>
      {(!settings.active_model) && <div className="text-yellow-400 mt-2 font-semibold">Prvo učitaj model prije promjene GPU/CPU postavki!</div>}
      {error && <div className="text-red-400 mt-2">{error}</div>}
      {success && <div className="text-green-400 mt-2">{success}</div>}
      <div className="mt-4 text-blue-200 text-sm">
        {settings.active_model ? (
          <span className="text-green-400 font-bold">Učitani model: {settings.active_model}</span>
        ) : (
          <span className="text-red-400">Nijedan model nije učitan.</span>
        )}
      </div>
    </div>
  );
}

export default AdminSettingsPanel;