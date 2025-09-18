import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import Card from '../components/Card';

interface AnalyticsData {
  total_subscribers: number;
  total_broadcasts: number;
  language_distribution: Record<string, number>;
  recent_broadcasts: number;
}

export default function Dashboard() {
  const weeklyRef = useRef<HTMLCanvasElement>(null);
  const languageRef = useRef<HTMLCanvasElement>(null);
  const [analytics, setAnalytics] = useState<AnalyticsData>({
    total_subscribers: 0,
    total_broadcasts: 0,
    language_distribution: {},
    recent_broadcasts: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch analytics data
    const fetchAnalytics = async () => {
      try {
        const response = await fetch('/api/analytics/stats');
        if (response.ok) {
          const data = await response.json();
          setAnalytics(data);
        }
      } catch (error) {
        console.error('Failed to fetch analytics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  useEffect(() => {
    let weeklyChart: Chart | null = null;
    let languageChart: Chart | null = null;

    if (weeklyRef.current && !loading) {
      // Weekly activity chart
      weeklyChart = new Chart(weeklyRef.current, {
        type: 'line',
        data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [
            {
              label: 'Messages Processed',
              data: [45, 67, 38, 89, 56, 42, 73],
              backgroundColor: 'rgba(220, 38, 38, 0.1)',
              borderColor: 'rgba(220, 38, 38, 1)',
              borderWidth: 3,
              fill: true,
              tension: 0.4,
              pointBackgroundColor: 'rgba(220, 38, 38, 1)',
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              pointRadius: 6,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: 'rgba(220, 38, 38, 1)',
              borderWidth: 1,
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(0, 0, 0, 0.05)' },
              ticks: { color: '#6b7280' }
            },
            x: {
              grid: { display: false },
              ticks: { color: '#6b7280' }
            }
          }
        },
      });
    }

    if (languageRef.current && !loading) {
      // Language distribution chart
      const langData = analytics.language_distribution;
      const languages = Object.keys(langData);
      const counts = Object.values(langData);
      
      if (languages.length > 0) {
        languageChart = new Chart(languageRef.current, {
          type: 'doughnut',
          data: {
            labels: languages.map(lang => {
              const langMap: Record<string, string> = {
                'en': 'English',
                'hi': 'Hindi',
                'or': 'Odia'
              };
              return langMap[lang] || lang;
            }),
            datasets: [
              {
                data: counts,
                backgroundColor: [
                  'rgba(34, 197, 94, 0.8)',
                  'rgba(59, 130, 246, 0.8)',
                  'rgba(234, 179, 8, 0.8)',
                  'rgba(239, 68, 68, 0.8)',
                ],
                borderColor: '#fff',
                borderWidth: 3,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  padding: 20,
                  usePointStyle: true,
                  color: '#6b7280'
                }
              },
              tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: '#fff',
                bodyColor: '#fff',
              }
            }
          },
        });
      }
    }

    return () => {
      weeklyChart?.destroy();
      languageChart?.destroy();
    };
  }, [analytics, loading]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-red-50 to-red-100 rounded-2xl p-6 border border-red-200">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-red-600 rounded-xl flex items-center justify-center">
            <span className="text-3xl text-white">🏥</span>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Welcome to Public Health Dashboard</h2>
            <p className="text-gray-600 mt-1">
              Monitor health awareness campaigns and manage community outreach programs
            </p>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card title="Total Subscribers">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">👥</span>
            </div>
            <div>
              <h3 className="text-3xl font-bold text-gray-800">{analytics.total_subscribers}</h3>
              <p className="text-sm text-gray-500">Active users</p>
            </div>
          </div>
        </Card>

        <Card title="Total Broadcasts">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">📢</span>
            </div>
            <div>
              <h3 className="text-3xl font-bold text-gray-800">{analytics.total_broadcasts}</h3>
              <p className="text-sm text-gray-500">Messages sent</p>
            </div>
          </div>
        </Card>

        <Card title="Recent Activity">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">⚡</span>
            </div>
            <div>
              <h3 className="text-3xl font-bold text-gray-800">{analytics.recent_broadcasts}</h3>
              <p className="text-sm text-gray-500">Recent alerts</p>
            </div>
          </div>
        </Card>

        <Card title="System Status">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">✅</span>
            </div>
            <div>
              <h3 className="text-xl font-bold text-green-600">Healthy</h3>
              <p className="text-sm text-gray-500">All systems operational</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Weekly Message Activity">
          <div className="h-64">
            <canvas ref={weeklyRef}></canvas>
          </div>
        </Card>

        <Card title="Language Distribution">
          <div className="h-64">
            <canvas ref={languageRef}></canvas>
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card title="Quick Actions">
          <div className="space-y-3">
            <button className="w-full bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg transition-colors duration-200 flex items-center gap-2">
              <span>📢</span>
              Send Alert
            </button>
            <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors duration-200 flex items-center gap-2">
              <span>👥</span>
              Manage Subscribers
            </button>
            <button className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition-colors duration-200 flex items-center gap-2">
              <span>📊</span>
              View Reports
            </button>
          </div>
        </Card>

        <Card title="Recent Alerts">
          <div className="space-y-3">
            <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
              <p className="text-sm font-medium text-yellow-800">Dengue Alert - Khordha</p>
              <p className="text-xs text-yellow-600 mt-1">2 hours ago</p>
            </div>
            <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-sm font-medium text-blue-800">Vaccination Drive - Cuttack</p>
              <p className="text-xs text-blue-600 mt-1">1 day ago</p>
            </div>
            <div className="p-3 bg-green-50 rounded-lg border border-green-200">
              <p className="text-sm font-medium text-green-800">Health Camp - Puri</p>
              <p className="text-xs text-green-600 mt-1">3 days ago</p>
            </div>
          </div>
        </Card>

        <Card title="System Health">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Backend API</span>
              <span className="text-green-600 text-sm font-medium">✅ Online</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Rasa NLP</span>
              <span className="text-green-600 text-sm font-medium">✅ Online</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">WhatsApp API</span>
              <span className="text-green-600 text-sm font-medium">✅ Connected</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Telegram API</span>
              <span className="text-green-600 text-sm font-medium">✅ Connected</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Database</span>
              <span className="text-green-600 text-sm font-medium">✅ Healthy</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}