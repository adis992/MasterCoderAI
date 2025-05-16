import React, { useState } from 'react';
import axios from 'axios';

function SimpleChatLayout() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

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

  return (
    <div className="h-screen w-screen flex flex-col bg-gray-900">
      <div className="flex-1 flex flex-col p-4 overflow-y-auto">
        {messages.length === 0 && (
          <div className="flex-1 flex items-center justify-center text-gray-400">
            <span>Send a message to start chatting...</span>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex mb-2 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <span className={`inline-block px-4 py-2 rounded-xl ${m.sender === 'user' ? 'bg-blue-700 text-white' : 'bg-gray-800 text-gray-100'}`}>
              {m.text}
            </span>
          </div>
        ))}
      </div>
      <div className="p-4 border-t border-gray-800">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Type your message..."
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            className="flex-1 p-2 bg-gray-800 text-white rounded-lg border border-gray-700"
          />
          <button 
            onClick={handleSend}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default SimpleChatLayout;
