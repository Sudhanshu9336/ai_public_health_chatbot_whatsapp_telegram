import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import LanguageBadge from '../components/LanguageBadge';

type Sub = { phone: string; language: string };

export default function Subscribers() {
  const [subs, setSubs] = useState<Sub[]>([]);
  useEffect(() => {
    fetch('/api/subscribers').then(r => r.json()).then(setSubs).catch(() => {});
  }, []);

  return (
    <Card title="All Subscribers">
      <div className="overflow-x-auto">
        <table className="w-full text-sm divide-y divide-gray-200">
          <thead>
            <tr className="text-left text-gray-500">
              <th className="py-2 px-3">Phone</th>
              <th className="py-2 px-3">Language</th>
            </tr>
          </thead>
          <tbody>
            {subs.map(s => (
              <tr key={s.phone} className="hover:bg-gray-50">
                <td className="py-2 px-3">{s.phone}</td>
                <td className="py-2 px-3"><LanguageBadge lang={s.language} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
