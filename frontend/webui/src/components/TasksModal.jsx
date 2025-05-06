import React, { useState, useEffect } from 'react';

function TasksModal({ user, onClose }) {
  const [taskText, setTaskText] = useState('');
  const [log, setLog] = useState([]);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const socket = new WebSocket(`ws://${window.location.host.replace(/:\d+/,':8000')}/ws/tasks`);
    socket.onopen = () => setLog(prev => [...prev, 'WebSocket connected']);
    socket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setLog(prev => [...prev, `Task ${data.task_id}: ${data.status}`]);
    };
    socket.onclose = () => setLog(prev => [...prev, 'WebSocket disconnected']);
    setWs(socket);

    return () => socket.close();
  }, []);

  const handleSubmit = () => {
    if (!taskText.trim()) return;
    const payload = { user_id: user.id, task: taskText };
    ws.send(JSON.stringify(payload));
    setLog(prev => [...prev, `Sent: ${taskText}`]);
    setTaskText('');
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-900 p-6 rounded-lg w-96 max-w-full">
        <h2 className="text-xl text-white mb-4">New Task</h2>
        <textarea
          className="w-full h-24 p-2 mb-4 bg-gray-800 text-white rounded"
          value={taskText}
          onChange={e => setTaskText(e.target.value)}
          placeholder="Describe your task..."
        />
        <div className="flex justify-end gap-2">
          <button className="px-4 py-2 bg-gray-700 text-white rounded" onClick={onClose}>Close</button>
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded" onClick={handleSubmit}>Submit</button>
        </div>
        <div className="mt-4 bg-gray-800 p-2 h-40 overflow-y-auto text-sm text-blue-200 rounded">
          {log.map((entry, i) => <div key={i}>{entry}</div>)}
        </div>
      </div>
    </div>
  );
}

export default TasksModal;