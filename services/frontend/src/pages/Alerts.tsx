import React, { useState, useEffect } from 'react';
import Card from '../components/Card';

interface BroadcastHistory {
  id: number;
  message: string;
  channel: string;
  timestamp: string;
}

export default function Alerts() {
  const [text, setText] = useState('🚨 Public Health Alert: Rising dengue cases reported in Khordha district. Please use mosquito nets, remove standing water, and seek medical attention for fever symptoms. Stay safe! 🏥');
  const [channel, setChannel] = useState<'whatsapp' | 'telegram'>('whatsapp');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<BroadcastHistory[]>([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch('/api/history');
      if (response.ok) {
        const data = await response.json();
        setHistory(data.slice(0, 10)); // Show last 10 broadcasts
      }
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  const sendBroadcast = async () => {
    if (!text.trim()) {
      setResult('❌ Please enter a message to broadcast');
      return;
    }

    setLoading(true);
    setResult('');

    try {
      const response = await fetch('/api/alerts/broadcast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, channel }),
      });

      const data = await response.json();
      
      if (response.ok && data.success) {
        setResult(`✅ Broadcast sent successfully!\n📊 Sent: ${data.sent} | Failed: ${data.failed} | Total: ${data.total}`);
        fetchHistory(); // Refresh history
      } else {
        setResult(`❌ Failed to send broadcast: ${data.message || 'Unknown error'}`);
      }
    } catch (error) {
      setResult(`❌ Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getChannelIcon = (channel: string) => {
    switch (channel.toLowerCase()) {
      case 'whatsapp':
        return '💬';
      case 'telegram':
        return '✈️';
      case 'sms':
        return '📱';
      default:
        return '📢';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-red-50 to-red-100 rounded-2xl p-6 border border-red-200">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-red-600 rounded-xl flex items-center justify-center">
            <span className="text-3xl text-white">📢</span>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Broadcast Health Alerts</h2>
            <p className="text-gray-600 mt-1">
              Send important health information to all subscribers instantly
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Broadcast Form */}
        <Card title="Send New Alert">
          <div className="space-y-4">
            {/* Message Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Alert Message
              </label>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="w-full border border-gray-300 rounded-xl p-4 focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-transparent resize-none transition-all duration-200"
                rows={6}
                placeholder="Enter your health alert message here..."
                maxLength={1000}
              />
              <div className="flex justify-between items-center mt-2">
                <span className="text-xs text-gray-500">
                  {text.length}/1000 characters
                </span>
                <span className="text-xs text-gray-500">
                  Include emojis for better engagement
                </span>
              </div>
            </div>

            {/* Channel Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Select Channel
              </label>
              <div className="flex gap-4">
                <label className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors duration-200">
                  <input
                    type="radio"
                    name="channel"
                    checked={channel === 'whatsapp'}
                    onChange={() => setChannel('whatsapp')}
                    className="accent-red-600"
                  />
                  <span className="text-2xl">💬</span>
                  <span className="font-medium text-gray-700">WhatsApp</span>
                </label>
                <label className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors duration-200">
                  <input
                    type="radio"
                    name="channel"
                    checked={channel === 'telegram'}
                    onChange={() => setChannel('telegram')}
                    className="accent-red-600"
                  />
                  <span className="text-2xl">✈️</span>
                  <span className="font-medium text-gray-700">Telegram</span>
                </label>
              </div>
            </div>

            {/* Send Button */}
            <button
              onClick={sendBroadcast}
              disabled={loading || !text.trim()}
              className="w-full bg-red-600 hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-bold py-3 px-6 rounded-xl shadow-lg transition-all duration-200 transform hover:-translate-y-1 active:translate-y-0 disabled:transform-none flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Sending...
                </>
              ) : (
                <>
                  <span>📤</span>
                  Send Alert
                </>
              )}
            </button>

            {/* Result Display */}
            {result && (
              <div className={`p-4 rounded-xl font-medium whitespace-pre-line ${
                result.startsWith('✅')
                  ? 'bg-green-50 text-green-800 border border-green-200'
                  : 'bg-red-50 text-red-800 border border-red-200'
              }`}>
                {result}
              </div>
            )}
          </div>
        </Card>

        {/* Quick Templates */}
        <Card title="Quick Templates">
          <div className="space-y-3">
            <div className="text-sm text-gray-600 mb-4">
              Click on a template to use it as your message:
            </div>
            
            {[
              {
                title: "Dengue Alert",
                message: "🚨 Dengue Alert: Cases rising in your area. Use mosquito nets, remove standing water, and consult a doctor for fever symptoms. Stay safe! 🏥"
              },
              {
                title: "Vaccination Drive",
                message: "💉 Vaccination Drive: Free vaccines available at your nearest health center. Protect yourself and your family. Book your slot today! 📅"
              },
              {
                title: "Health Camp",
                message: "🏥 Free Health Camp: General checkup, blood tests, and consultations available. Date: [DATE], Venue: [VENUE]. Don't miss this opportunity! 👩‍⚕️"
              },
              {
                title: "Monsoon Health Tips",
                message: "🌧️ Monsoon Health Tips: Drink boiled water, avoid street food, keep surroundings clean, and watch for fever symptoms. Stay healthy! 💪"
              }
            ].map((template, index) => (
              <button
                key={index}
                onClick={() => setText(template.message)}
                className="w-full text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors duration-200"
              >
                <div className="font-medium text-gray-800">{template.title}</div>
                <div className="text-sm text-gray-600 mt-1 line-clamp-2">
                  {template.message.substring(0, 100)}...
                </div>
              </button>
            ))}
          </div>
        </Card>
      </div>

      {/* Broadcast History */}
      <Card title="Recent Broadcasts">
        <div className="space-y-3">
          {history.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <span className="text-4xl mb-4 block">📭</span>
              <p>No broadcast history yet.</p>
              <p className="text-sm mt-1">Your sent alerts will appear here.</p>
            </div>
          ) : (
            history.map((broadcast) => (
              <div
                key={broadcast.id}
                className="p-4 border border-gray-200 rounded-xl bg-white hover:shadow-md transition-shadow duration-200"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-lg">{getChannelIcon(broadcast.channel)}</span>
                      <span className="text-sm font-medium text-gray-600 capitalize">
                        {broadcast.channel}
                      </span>
                      <span className="text-xs text-gray-400">•</span>
                      <span className="text-xs text-gray-500">
                        {formatTimestamp(broadcast.timestamp)}
                      </span>
                    </div>
                    <p className="text-gray-800 text-sm leading-relaxed">
                      {broadcast.message}
                    </p>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </Card>
    </div>
  );
}