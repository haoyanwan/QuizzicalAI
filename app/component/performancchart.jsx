import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const RecentPerformanceChart = () => {
  const chartRef = useRef(null);

  useEffect(() => {
    const ctx = chartRef.current.getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, 'rgba(75, 192, 192, 0.6)'); // Closer to the line, less transparent
    gradient.addColorStop(0.3, 'rgba(75, 192, 192, 0.4)');
    gradient.addColorStop(0.6, 'rgba(75, 192, 192, 0.2)');
    gradient.addColorStop(1, 'rgba(75, 192, 192, 0)'); // Further from the line, more transparent

    const data = {
      labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10'],
      datasets: [
        {
          label: 'Performance',
          data: [63, 78, 96, 53, 63, 71, 79, 61, 72, 73],
          fill: true,
          backgroundColor: gradient,
          borderColor: 'rgba(75, 192, 192, 1)',
          tension: 0.4,
        },
      ],
    };

    const options = {
      scales: {
        x: {
          display: false,
        },
        y: {
          display: false,
          beginAtZero: true, // Ensure the y-axis starts at 0
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
      elements: {
        line: {
          borderWidth: 2,
        },
        point: {
          radius: 0,
        },
      },
      maintainAspectRatio: false,
    };

    const myChart = new Chart(ctx, {
      type: 'line',
      data: data,
      options: options,
    });

    return () => {
      myChart.destroy();
    };
  }, []);

  return (
    <div className="p-1 rounded-lg" style={{ width: '400px', height: '250px' }}>
      <h2 className="text-xl font-semibold text-blue-800 mb-1">Recent Performance</h2>
      <canvas ref={chartRef} style={{ width: '100%', height: '80px' }}></canvas>
    </div>
  );
};

export default RecentPerformanceChart;
