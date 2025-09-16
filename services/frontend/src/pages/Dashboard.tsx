import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import Card from '../components/Card';

export default function Dashboard() {
  const weeklyRef = useRef<HTMLCanvasElement>(null);
  const volunteerRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    let weeklyChart: Chart | null = null;
    let volunteerChart: Chart | null = null;

    if (weeklyRef.current) {
      weeklyChart = new Chart(weeklyRef.current, {
        type: 'line',
        data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [
            {
              label: 'Programs Conducted',
              data: [5, 7, 3, 8, 6, 4, 9],
              backgroundColor: 'rgba(59,130,246,0.2)',
              borderColor: 'rgba(59,130,246,1)',
              borderWidth: 2,
              fill: true,
              tension: 0.3,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
        },
      });
    }

    if (volunteerRef.current) {
      volunteerChart = new Chart(volunteerRef.current, {
        type: 'doughnut',
        data: {
          labels: ['Doctors', 'Nurses', 'Volunteers', 'Admins'],
          datasets: [
            {
              data: [10, 15, 25, 8],
              backgroundColor: [
                'rgba(16,185,129,0.7)',
                'rgba(59,130,246,0.7)',
                'rgba(234,179,8,0.7)',
                'rgba(239,68,68,0.7)',
              ],
            },
          ],
        },
        options: { responsive: true },
      });
    }

    return () => {
      weeklyChart?.destroy();
      volunteerChart?.destroy();
    };
  }, []);

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <Card title="Total Outreach Programs">
          <h3 className="text-2xl font-bold">124</h3>
        </Card>
        <Card title="Active Volunteers">
          <h3 className="text-2xl font-bold">58</h3>
        </Card>
        <Card title="Communities Covered">
          <h3 className="text-2xl font-bold">36</h3>
        </Card>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <Card title="Weekly Outreach Activities">
          <canvas ref={weeklyRef} height={200}></canvas>
        </Card>
        <Card title="Volunteer Distribution">
          <canvas ref={volunteerRef} height={200}></canvas>
        </Card>
      </div>
    </div>
  );
}
