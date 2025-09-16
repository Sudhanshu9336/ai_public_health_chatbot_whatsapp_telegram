import React, { useState } from 'react';
import Card from '../components/Card';

export default function Alerts() {
  const [text, setText] = useState('Public health notice: Rising dengue cases in Khordha. Use nets/repellents and remove standing water.');
  const [result, setResult] = useState('');
  const [channel, setChannel] = useState<'whatsapp' | 'sms'>('whatsapp');

  async function send() {
    const r = await fetch('/api/alerts/broadcast', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, channel }),
    });
    setResult(JSON.stringify(await r.json(), null, 2));
  }

  return (
    <Card title="Broadcast Alert">
      <div className="space-y-4">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full border border-gray-300 rounded-2xl p-4 focus:outline-none focus:ring-2 focus:ring-red-600 resize-none transition-all duration-200"
          rows={5}
        />
        <div className="flex flex-wrap items-center gap-4">
          <label className="flex items-center gap-2 text-gray-700 cursor-pointer">
            <input type="radio" name="ch" checked={channel === 'whatsapp'} onChange={() => setChannel('whatsapp')} className="accent-red-600" />
            WhatsApp
          </label>
          <label className="flex items-center gap-2 text-gray-700 cursor-pointer">
            <input type="radio" name="ch" checked={channel === 'sms'} onChange={() => setChannel('sms')} className="accent-red-600" />
            SMS
          </label>
          <button
            onClick={send}
            className="bg-red-600 hover:bg-red-700 text-white font-bold px-6 py-2 rounded-2xl shadow-lg transition-transform transform hover:-translate-y-1"
          >
            Send
          </button>
        </div>
        {result && <pre className="bg-gray-50 p-4 rounded-2xl text-xs text-gray-800 overflow-x-auto shadow-inner">{result}</pre>}
      </div>
    </Card>
  );
}
