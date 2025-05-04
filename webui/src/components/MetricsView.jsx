import React from 'react';

function MetricsView() {
  return (
    <div className="metrics-view w-full h-full">
      <iframe
        src="/metrics"
        title="Metrics Dashboard"
        className="w-full h-screen border-0"
      />
    </div>
  );
}

export default MetricsView;
