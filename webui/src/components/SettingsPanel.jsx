import React, { useState, useEffect } from 'react';

function SettingsPanel() {
  const [model, setModel] = useState('default');
  const [temperature, setTemperature] = useState(0.7);
  const [darkMode, setDarkMode] = useState(false);
  
  // Apply dark mode class to document element
  useEffect(() => {
    if (darkMode) document.documentElement.classList.add('dark');
    else document.documentElement.classList.remove('dark');
  }, [darkMode]);

  const handleTrain = () => fetch('/train', { method: 'POST' });
  const handleBenchmark = () => fetch('/benchmark', { method: 'POST' });
  const handleMetrics = () => window.open('/metrics', '_blank');

  return (
    <aside className="settings-panel p-4 bg-white dark:bg-gray-800 shadow rounded w-full md:w-1/4">
      <h2 className="text-lg font-bold mb-4">Settings</h2>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Model</label>
        <select
          className="w-full border rounded p-2"
          value={model}
          onChange={e => setModel(e.target.value)}
        >
          <option value="default">Default Model</option>
          <option value="advanced">Advanced Model</option>
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Temperature: {temperature}</label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={temperature}
          onChange={e => setTemperature(parseFloat(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="mb-4 flex items-center">
        <label className="mr-2">Theme</label>
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="px-2 py-1 border rounded"
        >
          {darkMode ? 'Light' : 'Dark'}
        </button>
      </div>

      <div className="flex flex-col space-y-2">
        <button
          onClick={handleTrain}
          className="w-full bg-blue-500 text-white p-2 rounded"
        >Train Model</button>
        <button
          onClick={handleBenchmark}
          className="w-full bg-green-500 text-white p-2 rounded"
        >Run Benchmark</button>
        <button
          onClick={handleMetrics}
          className="w-full bg-gray-500 text-white p-2 rounded"
        >View Metrics</button>
      </div>
    </aside>
  );
}

export default SettingsPanel;