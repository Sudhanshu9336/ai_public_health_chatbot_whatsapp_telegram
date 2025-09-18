import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import LanguageBadge from '../components/LanguageBadge';

interface Subscriber {
  phone: string;
  language: string;
}

export default function Subscribers() {
  const [subscribers, setSubscribers] = useState<Subscriber[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('all');

  useEffect(() => {
    fetchSubscribers();
  }, []);

  const fetchSubscribers = async () => {
    try {
      const response = await fetch('/api/subscribers');
      if (response.ok) {
        const data = await response.json();
        setSubscribers(data);
      } else {
        console.error('Failed to fetch subscribers');
      }
    } catch (error) {
      console.error('Error fetching subscribers:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeSubscriber = async (phone: string) => {
    if (!confirm(`Are you sure you want to remove subscriber ${phone}?`)) {
      return;
    }

    try {
      const response = await fetch(`/api/subscribers/${encodeURIComponent(phone)}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setSubscribers(prev => prev.filter(sub => sub.phone !== phone));
      } else {
        alert('Failed to remove subscriber');
      }
    } catch (error) {
      console.error('Error removing subscriber:', error);
      alert('Error removing subscriber');
    }
  };

  // Filter subscribers based on search and language
  const filteredSubscribers = subscribers.filter(subscriber => {
    const matchesSearch = subscriber.phone.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLanguage = selectedLanguage === 'all' || subscriber.language === selectedLanguage;
    return matchesSearch && matchesLanguage;
  });

  // Get language statistics
  const languageStats = subscribers.reduce((acc, sub) => {
    acc[sub.language] = (acc[sub.language] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading subscribers...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-2xl p-6 border border-blue-200">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-blue-600 rounded-xl flex items-center justify-center">
            <span className="text-3xl text-white">👥</span>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Subscriber Management</h2>
            <p className="text-gray-600 mt-1">
              Manage your health alert subscribers and view engagement statistics
            </p>
          </div>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card title="Total Subscribers">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">👥</span>
            </div>
            <div>
              <h3 className="text-3xl font-bold text-gray-800">{subscribers.length}</h3>
              <p className="text-sm text-gray-500">Active users</p>
            </div>
          </div>
        </Card>

        <Card title="English Users">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">🇬🇧</span>
            </div>
            <div>
              <h3 className="text-3xl font-bold text-gray-800">{languageStats.en || 0}</h3>
              <p className="text-sm text-gray-500">English speakers</p>
            </div>
          </div>
        </Card>

        <Card title="Hindi Users">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">🇮🇳</span>
            </div>
            <div>
              <h3 className="text-3xl font-bold text-gray-800">{languageStats.hi || 0}</h3>
              <p className="text-sm text-gray-500">Hindi speakers</p>
            </div>
          </div>
        </Card>

        <Card title="Odia Users">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">🏛️</span>
            </div>
            <div>
              <h3 className="text-3xl font-bold text-gray-800">{languageStats.or || 0}</h3>
              <p className="text-sm text-gray-500">Odia speakers</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Filters and Search */}
      <Card title="Subscriber List">
        <div className="space-y-4">
          {/* Search and Filter Controls */}
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search by phone number..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
              />
            </div>
            <div className="md:w-48">
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
              >
                <option value="all">All Languages</option>
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="or">Odia</option>
              </select>
            </div>
          </div>

          {/* Results Summary */}
          <div className="text-sm text-gray-600">
            Showing {filteredSubscribers.length} of {subscribers.length} subscribers
          </div>

          {/* Subscribers Table */}
          <div className="overflow-x-auto rounded-xl border border-gray-200">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Phone Number
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Language
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredSubscribers.length === 0 ? (
                  <tr>
                    <td colSpan={3} className="px-6 py-12 text-center text-gray-500">
                      <div className="flex flex-col items-center">
                        <span className="text-4xl mb-4">👤</span>
                        <p className="text-lg font-medium">No subscribers found</p>
                        <p className="text-sm mt-1">
                          {searchTerm || selectedLanguage !== 'all' 
                            ? 'Try adjusting your search or filter criteria'
                            : 'Subscribers will appear here once they join your health alerts'
                          }
                        </p>
                      </div>
                    </td>
                  </tr>
                ) : (
                  filteredSubscribers.map((subscriber) => (
                    <tr key={subscriber.phone} className="hover:bg-gray-50 transition-colors duration-200">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center mr-3">
                            <span className="text-lg">📱</span>
                          </div>
                          <div>
                            <div className="text-sm font-medium text-gray-900">
                              {subscriber.phone}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <LanguageBadge lang={subscriber.language} />
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button
                          onClick={() => removeSubscriber(subscriber.phone)}
                          className="text-red-600 hover:text-red-900 transition-colors duration-200 px-3 py-1 rounded-md hover:bg-red-50"
                        >
                          Remove
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination could be added here for large datasets */}
        </div>
      </Card>
    </div>
  );
}