import React, { useState, useEffect, useRef, useContext } from 'react';
import axios from 'axios';
import LibraryGallery from './LibraryGallery';
import { AuthContext } from '../context/AuthContext';
import TasksModal from './TasksModal';

const DUMMY_SESSIONS = [
  { id: 1, name: 'New Chat', isNew: true },
  { id: 2, name: 'Prompt: How to deploy FastAPI?' },
  { id: 3, name: 'Prompt: Explain transformers' },
];

function ChatLayout() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [tasksOpen, setTasksOpen] = useState(false);
  const [sessions, setSessions] = useState(DUMMY_SESSIONS);
  const [activeSession, setActiveSession] = useState(DUMMY_SESSIONS[0].id);
  const messagesEndRef = useRef(null);
  const { user } = useContext(AuthContext);
  const saveKey = `chat_${user?.id}`;
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const fileInputRef = useRef();
  const [isDownloading, setIsDownloading] = useState(false);
  const [gpus, setGpus] = useState([]);
  const [showHfInput, setShowHfInput] = useState(false);
  const [hfModel, setHfModel] = useState('');
  const [uploading, setUploading] = useState(false);
  const [gpuSelection, setGpuSelection] = useState([]);

  useEffect(() => {
    document.documentElement.classList.add('dark');
    // Load chat history
    const stored = localStorage.getItem(saveKey);
    if (stored) {
      setMessages(JSON.parse(stored));
    } else {
      axios.get(`${process.env.REACT_APP_API_URL || ''}/chats`)
        .then(res => {
          const msgs = res.data.flatMap(c => [
            { sender: 'user', text: c.message },
            { sender: 'bot', text: c.response }
          ]);
          setMessages(msgs);
          localStorage.setItem(saveKey, JSON.stringify(msgs));
        });
    }
    axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/models`)
      .then(res => {
        setModels(res.data.models || []);
        setGpus(res.data.gpus || []);
      })
      .catch(console.error);
    axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/settings`)
      .then(res => {
        setGpuSelection(Array.isArray(res.data.gpu_enabled) ? res.data.gpu_enabled : []);
      })
      .catch(console.error);
  }, [saveKey]);

  const handleModelUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      await axios.post(`${process.env.REACT_APP_API_URL || ''}/admin/upload_model`, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
      // Refresh model list
      const res = await axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/models`);
      setModels(res.data.models || []);
    } catch (err) {
      alert('Upload failed!');
    }
    setUploading(false);
  };

  const handleHuggingFaceDownload = async () => {
    const repo = prompt('Unesi Hugging Face repo/model npr. "TheBloke/Llama-2-7B-GGUF"');
    if (!repo) return;
    setIsDownloading(true);
    try {
      await axios.post(`${process.env.REACT_APP_API_URL || ''}/admin/download_model`, { repo });
      const res = await axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/models`);
      setModels(res.data.models || []);
    } finally {
      setIsDownloading(false);
    }
  };

  const handleHfDownload = async () => {
    if (!hfModel) return;
    setUploading(true);
    try {
      await axios.post(`${process.env.REACT_APP_API_URL || ''}/admin/download_model`, { model: hfModel });
      // Refresh model list
      const res = await axios.get(`${process.env.REACT_APP_API_URL || ''}/admin/models`);
      setModels(res.data.models || []);
      setShowHfInput(false);
      setHfModel('');
    } catch (err) {
      alert('Download failed!');
    }
    setUploading(false);
  };

  const toggleGpu = id => {
    setGpuSelection(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
    // Optionally, send to backend here
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    const newMsgs = [...messages, { sender: 'user', text: input }];
    setMessages(newMsgs);
    setInput('');
    try {
      const res = await axios.post(`${process.env.REACT_APP_API_URL || ''}/chat`, { message: input });
      const botMsg = { sender: 'bot', text: res.data.response };
      const allMsgs = [...newMsgs, botMsg];
      setMessages(allMsgs);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  // New: right sidebar options for bot features
  const rightOptions = [
    { label: 'Enable Web Search', type: 'toggle', default: false },
    { label: 'Allowed Sites', type: 'input', default: 'wikipedia.org, stackoverflow.com' },
    { label: 'Auto Scrape Data', type: 'button', action: () => alert('Auto-scraping...') },
    { label: 'Enable Plugins', type: 'toggle', default: false },
    { label: 'Enable Vision', type: 'toggle', default: false },
    { label: 'Enable File Upload', type: 'toggle', default: false },
    { label: 'Enable Image Output', type: 'toggle', default: false },
    { label: 'Enable Memory', type: 'toggle', default: false },
    { label: 'Enable Voice', type: 'toggle', default: false },
    { label: 'Enable Code', type: 'toggle', default: false },
  ];

  // Settings options for the settings modal
  const settingsOptions = [
    { label: 'Model', type: 'select', options: ['GPT-4', 'GPT-3.5', 'Mixtral', 'Llama', 'Custom'] },
    { label: 'Temperature', type: 'slider', min: 0, max: 1, step: 0.01, default: 0.7 },
    { label: 'Max Tokens', type: 'slider', min: 128, max: 4096, step: 32, default: 1024 },
    { label: 'Top P', type: 'slider', min: 0, max: 1, step: 0.01, default: 1 },
    { label: 'Presence Penalty', type: 'slider', min: -2, max: 2, step: 0.01, default: 0 },
    { label: 'Frequency Penalty', type: 'slider', min: -2, max: 2, step: 0.01, default: 0 },
    { label: 'System Prompt', type: 'textarea', default: '' },
    { label: 'Stop Sequences', type: 'input', default: '' },
    { label: 'Streaming', type: 'toggle', default: true },
    { label: 'Auto Save', type: 'toggle', default: false },
    { label: 'Show Tokens', type: 'toggle', default: false },
    { label: 'Show Probabilities', type: 'toggle', default: false },
    { label: 'Enable Plugins', type: 'toggle', default: false },
    { label: 'Enable Vision', type: 'toggle', default: false },
    { label: 'Enable Code', type: 'toggle', default: false },
    { label: 'Enable Voice', type: 'toggle', default: false },
    { label: 'Theme', type: 'select', options: ['System', 'Light', 'Dark'] },
    { label: 'Font Size', type: 'slider', min: 12, max: 24, step: 1, default: 16 },
    { label: 'Chat Width', type: 'slider', min: 400, max: 1200, step: 20, default: 700 },
    { label: 'Sidebar Width', type: 'slider', min: 180, max: 400, step: 10, default: 280 },
    { label: 'Show Avatars', type: 'toggle', default: true },
    { label: 'Show Timestamps', type: 'toggle', default: false },
    { label: 'Show Markdown', type: 'toggle', default: true },
    { label: 'Show Syntax Highlight', type: 'toggle', default: true },
    { label: 'Show Metrics', type: 'toggle', default: false },
    { label: 'Show Logs', type: 'toggle', default: false },
  ];

  // Provjera: da li je model učitan ili postoji API ključ
  const modelLoaded = models && models.length > 0;
  const apiKey = process.env.REACT_APP_OPENAI_API_KEY || '';
  const canChat = modelLoaded || apiKey;

  return (
    // Use flex-1 container to respect parent layout, not full viewport size
    <div className="flex-1 flex flex-col bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
      {/* Centered Top Menu */}
      <nav className="w-full flex items-center justify-center px-6 h-14 bg-gray-950 border-b border-blue-900 shadow z-50 relative">
        <div className="flex items-center gap-4 absolute left-4">
          <span className="font-bold text-blue-400 text-lg tracking-wide">MasterCoderAI</span>
          {/* Removed Admin Panel button from left side, now only in AdminPanel.jsx top right */}
        </div>
        <div className="flex items-center gap-4">
          <select
            className="bg-gray-900 text-blue-200 rounded px-2 py-1 border border-blue-900 max-w-[220px] truncate text-ellipsis text-sm font-semibold"
            style={{ minWidth: '120px', maxWidth: '220px', width: 'auto', overflow: 'hidden', textOverflow: 'ellipsis' }}
            value={selectedModel}
            onChange={e => setSelectedModel(e.target.value)}
          >
            <option value="">Model: None</option>
            {models.map(m => (
              <option key={m} value={m} className="truncate">Model: {m}</option>
            ))}
          </select>
          {/* Novi upload button koji koristi fileInputRef */}
          <button
            className="bg-gray-900 text-blue-200 rounded px-2 py-1 border border-blue-900"
            onClick={() => fileInputRef.current && fileInputRef.current.click()}
            disabled={uploading}
          >
            {uploading ? 'Uploading...' : 'Upload model'}
          </button>
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleModelUpload}
            disabled={uploading}
          />
          {/* Dugme za prompt-based HuggingFace download */}
          <button
            className="bg-gray-900 text-blue-200 rounded px-2 py-1 border border-blue-900"
            onClick={handleHuggingFaceDownload}
            disabled={isDownloading}
          >
            {isDownloading ? 'Downloading...' : 'Download HuggingFace Model'}
          </button>
          {/* Postojeći flow za custom HF download */}
          <button
            className="bg-gray-900 text-blue-200 rounded px-2 py-1 border border-blue-900"
            onClick={() => setShowHfInput(v => !v)}
            disabled={uploading}
          >
            Download from HuggingFace
          </button>
          {showHfInput && (
            <div className="flex items-center gap-2">
              <input
                className="bg-gray-800 text-blue-200 rounded px-2 py-1 border border-blue-900"
                placeholder="huggingface/model-name"
                value={hfModel}
                onChange={e => setHfModel(e.target.value)}
                disabled={uploading}
              />
              <button className="bg-blue-700 text-white rounded px-2 py-1" onClick={handleHfDownload} disabled={uploading}>OK</button>
            </div>
          )}
          <button
            className="bg-gray-900 text-blue-200 rounded px-2 py-1 border border-blue-900"
            onClick={() => window.open('https://vscode.dev/', '_blank')}
          >
            Otvori VSC
          </button>
        </div>
        {/* GPU Dropdown to prevent overlap */}
        <div className="relative">
          <details className="group">
            <summary className="flex items-center gap-2 cursor-pointer bg-gray-900 text-blue-200 rounded px-2 py-1 border border-blue-900 select-none">
              GPUs <span className="ml-1">({gpus.length})</span>
            </summary>
            <div className="absolute right-0 mt-2 w-64 max-h-60 overflow-y-auto bg-gray-950 border border-blue-900 rounded-lg shadow-lg z-50 p-2 flex flex-col gap-2">
              {gpus.map(gpu => (
                <label key={gpu.id} className="flex items-center text-blue-200 whitespace-nowrap">
                  <input type="checkbox" className="mr-1" checked={gpuSelection.includes(gpu.id)} onChange={() => toggleGpu(gpu.id)} />
                  {gpu.name} (ID: {gpu.id})
                </label>
              ))}
            </div>
          </details>
        </div>
        <button className="absolute right-4 text-2xl text-blue-300" onClick={() => setSettingsOpen(true)}>⚙️</button>
      </nav>

      <div className="flex flex-1 min-h-0 w-full">
        {/* Left Sidebar (responsive, auto size) */}
        <aside className="hidden md:flex flex-col w-64 max-w-xs min-w-[180px] bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 border-r-2 border-blue-900 shadow-xl p-0 max-h-full ml-2 rounded-xl">
          <div className="flex items-center justify-between h-16 px-4 border-b border-blue-900">
            <span className="font-bold text-lg tracking-wide text-blue-300">Chats</span>
          </div>
          <button
            className="m-4 w-[90%] py-2 rounded-lg bg-blue-700 hover:bg-blue-800 text-white font-semibold shadow flex items-center justify-center text-center"
            onClick={() => {
              const newId = sessions.length + 1;
              setSessions([{ id: newId, name: 'New Chat', isNew: true }, ...sessions]);
              setActiveSession(newId);
              setMessages([]);
            }}
          >+ New Chat</button>
          <div className="flex-1 overflow-y-auto px-2 pb-4">
            {sessions.map(s => (
              <button
                key={s.id}
                className={`w-full text-center px-4 py-2 my-1 rounded-lg transition-colors ${activeSession === s.id ? 'bg-blue-900 font-bold text-blue-200' : 'hover:bg-gray-800 text-blue-100'}`}
                onClick={() => { setActiveSession(s.id); setMessages([]); }}
              >{s.name}</button>
            ))}
          </div>
          <div className="p-2 border-t border-blue-900">
            <LibraryGallery />
          </div>
          {/* Bottom border */}
          <div className="w-full mt-2 mb-2 border-b-2 border-blue-900 rounded-full"></div>
        </aside>

        {/* Main Chat Area (responsive) */}
        <main className="flex-1 flex flex-col items-center px-2 min-h-0 relative bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
          <div className="w-full min-w-[320px] flex flex-col flex-1 bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 rounded-2xl shadow-2xl p-0 min-h-[70vh] border border-blue-900 relative h-full mb-[6px]">
            {/* Chat and footer always at the bottom, no gap, no horizontal scroll */}
            <div className="flex flex-col flex-1 justify-end">
              <div className="flex-1 flex flex-col-reverse overflow-y-auto px-4 pb-0 pt-0" style={{ maxHeight: '60vh', overflowX: 'hidden' }}>
                <div ref={messagesEndRef} />
                {messages.length === 0 && (
                  <div className="flex flex-col items-center justify-center h-full text-blue-900 select-none">
                    <span className="mt-2 text-lg">Message ChatGPT…</span>
                  </div>
                )}
                {[...messages].reverse().map((m, i) => (
                  <div key={i} className={`flex mb-2 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`rounded-lg px-4 py-2 ${m.sender === 'user' ? 'bg-blue-800 text-white' : 'bg-gray-800 text-blue-200'}`}>{m.text}</div>
                  </div>
                ))}
              </div>
            </div>
            {/* Disable chat input ako nema modela ili API ključa */}
            {!canChat && (
              <div className="w-full text-center text-red-400 font-bold py-4 bg-gray-900 border-t border-blue-900">
                Chat disabled: No model loaded and no API key set.
              </div>
            )}
            <div className="p-4 border-t border-gray-800 flex gap-2">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder={canChat ? "Type your message..." : "Chat disabled until model/API key"}
                onKeyDown={e => e.key === 'Enter' && canChat && handleSend()}
                className="flex-1 p-2 bg-gray-800 text-white rounded-lg border border-gray-700"
                disabled={!canChat}
              />
              <button
                onClick={handleSend}
                disabled={!canChat}
                className={`px-4 py-2 rounded-lg font-bold ${canChat ? 'bg-blue-700 hover:bg-blue-800 text-white' : 'bg-gray-700 text-gray-400 cursor-not-allowed'}`}
              >Send</button>
            </div>
          </div>
        </main>

        {/* Right Sidebar (responsive, auto size) */}
        <aside className="hidden md:flex flex-col w-64 max-w-xs min-w-[180px] bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 border-l-2 border-blue-900 shadow-xl p-0 max-h-[calc(100vh-56px)] mr-2 rounded-xl">
          <div className="flex items-center justify-between h-16 px-4 border-b border-blue-900">
            <span className="font-bold text-lg tracking-wide text-blue-300">Bot Options</span>
          </div>
          <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4 custom-scrollbar">
            {rightOptions.map(opt => (
              <div key={opt.label} className="flex flex-col gap-1 bg-gray-900 rounded-lg p-3 shadow border border-blue-900">
                <label className="font-semibold text-sm mb-1 text-blue-200">{opt.label}</label>
                {opt.type === 'toggle' && (
                  <input type="checkbox" defaultChecked={opt.default} />
                )}
                {opt.type === 'input' && (
                  <input type="text" className="p-2 rounded border bg-gray-950 text-blue-100" defaultValue={opt.default} />
                )}
                {opt.type === 'button' && (
                  <button onClick={opt.action} className="p-2 rounded bg-blue-700 text-white font-semibold hover:bg-blue-800">{opt.label}</button>
                )}
              </div>
            ))}
          </div>
          {/* Bottom border */}
          <div className="w-[90%] mx-auto mt-2 mb-2 border-b-2 border-blue-900 rounded-full"></div>
        </aside>

        {/* Settings floating button (bottom right, always visible) */}
        <button
          className="fixed bottom-6 right-6 z-50 bg-blue-700 hover:bg-blue-800 text-white rounded-full p-4 shadow-xl lg:hidden"
          onClick={() => setSettingsOpen(true)}
        >⚙️</button>

        {/* Settings Modal - 3-4 columns, blurred background, visually appealing, never taller than chat, with Save/Cancel */}
        {settingsOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm">
            <div className="bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 rounded-2xl shadow-2xl border-4 border-blue-900 w-full max-w-4xl p-10 relative mx-2 max-h-[80vh] overflow-y-auto flex flex-col">
              <button className="absolute top-4 right-4 text-2xl text-blue-300" onClick={() => setSettingsOpen(false)}>✕</button>
              <button className="absolute top-4 right-4 text-2xl text-blue-300" onClick={() => setSettingsOpen(false)}>✕</button>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {settingsOptions.map(opt => (
                  <div key={opt.label} className="flex flex-col gap-1 bg-gray-900 rounded-lg p-3 shadow border border-blue-900">
                    <label className="font-semibold text-sm mb-1 text-blue-200">{opt.label}</label>
                    {opt.type === 'select' && (
                      <select className="p-2 rounded border bg-gray-950 text-blue-100">
                        {opt.options.map(o => (
                          <option key={o} value={o}>{o}</option>
                        ))}
                      </select>
                    )}
                    {opt.type === 'slider' && (
                      <input type="range" min={opt.min} max={opt.max} step={opt.step} defaultValue={opt.default} />
                    )}
                    {opt.type === 'toggle' && (
                      <input type="checkbox" defaultChecked={opt.default} />
                    )}
                    {opt.type === 'input' && (
                      <input type="text" className="p-2 rounded border bg-gray-950 text-blue-100" defaultValue={opt.default} />
                    )}
                    {opt.type === 'textarea' && (
                      <textarea className="p-2 rounded border bg-gray-950 text-blue-100" defaultValue={opt.default} />
                    )}
                  </div>
                ))}
              </div>
              <div className="flex justify-end gap-4 mt-8">
                <button className="px-6 py-2 rounded-lg bg-blue-700 hover:bg-blue-800 text-white font-semibold shadow" onClick={() => setSettingsOpen(false)}>Cancel</button>
                <button className="px-6 py-2 rounded-lg bg-blue-500 hover:bg-blue-600 text-white font-semibold shadow">Save</button>
              </div>
            </div>
          </div>
        )}
        {tasksOpen && <TasksModal user={user} onClose={() => setTasksOpen(false)} />}
      </div>
    </div>
  );
}

export default ChatLayout;