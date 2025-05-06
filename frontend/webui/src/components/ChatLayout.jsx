import React, { useState, useEffect, useRef, useContext } from 'react';
import axios from 'axios';
import LibraryGallery from './LibraryGallery';
import SettingsPanel from './SettingsPanel';
import { AuthContext } from '../context/AuthContext';
import TasksModal from './TasksModal';
import { useNavigate } from 'react-router-dom';

const DUMMY_SESSIONS = [
  { id: 1, name: 'New Chat', isNew: true },
  { id: 2, name: 'Prompt: How to deploy FastAPI?' },
  { id: 3, name: 'Prompt: Explain transformers' },
];

function ChatLayout() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [tasksOpen, setTasksOpen] = useState(false);
  const [sessions, setSessions] = useState(DUMMY_SESSIONS);
  const [activeSession, setActiveSession] = useState(DUMMY_SESSIONS[0].id);
  const messagesEndRef = useRef(null);
  const { user } = useContext(AuthContext);
  const saveKey = `chat_${user?.id}`;
  const navigate = useNavigate();

  useEffect(() => {
    document.documentElement.classList.add('dark');
    // Load chat history
    const stored = localStorage.getItem(saveKey);
    if (stored) {
      setMessages(JSON.parse(stored));
    } else {
      axios.get('/chats')
        .then(res => {
          const msgs = res.data.flatMap(c => [
            { sender: 'user', text: c.message },
            { sender: 'bot', text: c.response }
          ]);
          setMessages(msgs);
          localStorage.setItem(saveKey, JSON.stringify(msgs));
        });
    }
  }, [saveKey]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input };
    const newMsgs = [...messages, userMsg];
    setMessages(newMsgs);
    localStorage.setItem(saveKey, JSON.stringify(newMsgs));
    setInput('');
    try {
      const res = await axios.post('/chat', { message: input });
      const botMsg = { sender: 'bot', text: res.data.response };
      const allMsgs = [...newMsgs, botMsg];
      setMessages(allMsgs);
      localStorage.setItem(saveKey, JSON.stringify(allMsgs));
    } catch (err) {
      console.error(err);
    }
  };

  // Opcije za prompt i model tuning
  const promptOptions = [
    { label: 'Regenerate', icon: '🔄' },
    { label: 'Stop', icon: '⏹️' },
    { label: 'Copy', icon: '📋' },
    { label: 'Mic', icon: '🎤' },
    { label: 'Upload', icon: '📎' },
    { label: 'Clear', icon: '🧹' },
    { label: 'Save', icon: '💾' },
    { label: 'Share', icon: '🔗' },
    { label: 'Export', icon: '⬇️' },
    { label: 'Import', icon: '⬆️' },
  ];

  // 20+ naprednih opcija za desni panel
  const settingsOptions = [
    { label: 'Model', type: 'select', options: ['GPT-4', 'GPT-3.5', 'Mixtral', 'Llama', 'Custom'] },
    { label: 'Temperature', type: 'slider', min: 0, max: 1, step: 0.01, default: 0.7 },
    { label: 'Max Tokens', type: 'slider', min: 128, max: 4096, step: 32, default: 1024 },
    { label: 'Top P', type: 'slider', min: 0, max 1, step: 0.01, default: 1 },
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
    { label: 'Enable Web Search', type: 'toggle', default: false },
    { label: 'Enable Memory', type: 'toggle', default: false },
    { label: 'Enable File Upload', type: 'toggle', default: false },
    { label: 'Enable Image Output', type: 'toggle', default: false },
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

  return (
    <div className="h-screen w-screen flex flex-col bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
      {/* Centered Top Menu */}
      <nav className="w-full flex items-center justify-center px-6 h-14 bg-gray-950 border-b border-blue-900 shadow z-50 relative">
        <div className="flex items-center gap-4 absolute left-4">
          <span className="font-bold text-blue-400 text-lg tracking-wide">MasterCoderAI</span>
          {user?.is_admin && (
            <button onClick={() => navigate('/admin')} className="text-blue-200 hover:underline">
              Admin Panel
            </button>
          )}
        </div>
        <div className="flex items-center gap-4">
          <select className="bg-gray-900 text-blue-200 rounded px-2 py-1 border border-blue-900">
            <option>Model: GPT-4</option>
            <option>Model: Mixtral</option>
            <option>Model: Llama</option>
            <option>Model: Custom</option>
          </select>
          <select className="bg-gray-900 text-blue-200 rounded px-2 py-1 border border-blue-900">
            <option>VSC: VSCode</option>
            <option>VSC: NeoVim</option>
          </select>
          <select className="bg-gray-900 text-blue-200 rounded px-2 py-1 border border-blue-900">
            <option>GPU: 3090</option>
            <option>GPU: 1080Ti</option>
            <option>CPU: 12c/24t</option>
          </select>
          <button onClick={() => setTasksOpen(true)} className="text-blue-200">Zadaci</button>
        </div>
        <button className="absolute right-4 text-2xl text-blue-300" onClick={() => setSettingsOpen(true)}>⚙️</button>
      </nav>

      <div className="flex flex-1 min-h-0 w-full">
        {/* Left Sidebar with margin and bottom border */}
        <aside className="hidden lg:flex flex-col w-72 bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 border-r-2 border-blue-900 shadow-xl p-0 max-h-[calc(100vh-56px)] ml-2 rounded-xl">
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
          <div className="w-[90%] mx-auto mt-2 mb-2 border-b-2 border-blue-900 rounded-full"></div>
        </aside>

        {/* Main Chat Area with more space from sidebars and single-row prompt options */}
        <main className="flex-1 flex flex-col items-center px-2 min-h-0 relative bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
          <div className="w-full max-w-[calc(100vw-340px-340px-32px)] min-w-[700px] flex flex-col flex-1 bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 rounded-2xl shadow-2xl p-0 min-h-[70vh] border border-blue-900 relative h-full mx-auto mb-[6px]">
            {/* Chat and footer always at the bottom, no gap, no horizontal scroll */}
            <div className="flex flex-col flex-1 justify-end">
              <div className="flex-1 flex flex-col-reverse overflow-y-auto px-8 pb-0 pt-0" style={{ maxHeight: '60vh', overflowX: 'hidden' }}>
                <div ref={messagesEndRef} />
                {messages.length === 0 && (
                  <div className="flex flex-col items-center justify-center h-full text-blue-900 select-none">
                    <svg width="48" height="48" fill="none" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
                    <span className="mt-2 text-lg">Message ChatGPT…</span>
                  </div>
                )}
                {[...messages].reverse().map((m, i) => (
                  <div key={i} className={`flex mb-2 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <span className={`inline-block px-4 py-2 rounded-2xl shadow ${m.sender === 'user' ? 'bg-blue-700 text-white' : 'bg-blue-950 text-blue-100'}`}>{m.text}</span>
                  </div>
                ))}
              </div>
              {/* Input and prompt options, footer flush with bottom, no extra margin */}
              <div className="w-full px-8 pb-0 pt-2 bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 rounded-b-2xl border-t border-blue-900">
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    placeholder="Message ChatGPT..."
                    onKeyDown={e => e.key === 'Enter' && handleSend()}
                    className="flex-1 p-3 border border-blue-900 rounded-xl bg-gray-900 text-blue-100 shadow"
                  />
                  <button onClick={handleSend} className="p-3 px-6 bg-blue-700 hover:bg-blue-800 text-white rounded-xl shadow font-semibold">Send</button>
                </div>
                <div className="flex gap-2 justify-center min-w-[700px] max-w-full overflow-x-auto whitespace-nowrap mb-2">
                  {promptOptions.map(opt => (
                    <button key={opt.label} className="flex items-center justify-center gap-1 px-3 py-1 rounded bg-blue-950 text-blue-200 hover:bg-blue-900 transition text-sm font-medium text-center">
                      <span>{opt.icon}</span>
                      <span className="sm:inline">{opt.label}</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </main>

        {/* Right Sidebar with margin and bottom border, visually balanced with left, scrollable */}
        <aside className="hidden lg:flex flex-col w-72 bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 border-l-2 border-blue-900 shadow-xl p-0 max-h-[calc(100vh-56px)] mr-2 rounded-xl">
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
              <div className="text-2xl font-bold text-blue-300 mb-6 text-center">Settings</div>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 flex-shrink-0">
                {settingsOptions.map((opt, idx) => (
                  <div key={opt.label} className="flex flex-col gap-1 bg-gray-900 rounded-lg p-4 shadow border border-blue-900">
                    <label className="font-semibold text-sm mb-1 text-blue-200">{opt.label}</label>
                    {opt.type === 'select' && (
                      <select className="p-2 rounded border bg-gray-950 text-blue-100">
                        {opt.options.map(o => <option key={o}>{o}</option>)}
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