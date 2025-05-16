// filepath: src/components/AnalyticsPanel.jsx
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function AnalyticsPanel() {
  const [data, setData] = useState({ labels: [], datasets: [] });
  const API_URL = process.env.REACT_APP_API_URL || '';

  useEffect(() => {
    axios.get(`${API_URL}/admin/analytics`)
      .then(res => {
        const raw = res.data;
        const labels = raw.timestamps;
        const datasets = raw.metrics.map(m => ({
          label: m.name,
          data: m.values,
          borderColor: m.color || 'rgba(75,192,192,1)',
          backgroundColor: m.color ? m.color.replace('1)', '0.2)') : 'rgba(75,192,192,0.2)',
        }));
        setData({ labels, datasets });
      })
      .catch(err => console.error(err));
  }, [API_URL]);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4 text-white">Analytics Dashboard</h2>
      <Line
        data={data}
        options={{
          responsive: true,
          plugins: {
            legend: { position: 'top' },
            title: { display: true, text: 'System Metrics Over Time', color: '#fff' },
          },
          scales: {
            x: { ticks: { color: '#fff' } },
            y: { ticks: { color: '#fff' } }
          }
        }}
      />
    </div>
  );
}

export default AnalyticsPanel;
