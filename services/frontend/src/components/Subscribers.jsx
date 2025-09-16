import { useEffect, useState } from "react";

export default function Subscribers() {
  const [subs, setSubs] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/subscribers")
      .then((res) => res.json())
      .then(setSubs)
      .catch(() => setSubs([]));
  }, []);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="max-w-4xl mx-auto bg-white shadow-2xl rounded-2xl p-6">
        <h2 className="text-2xl font-extrabold mb-6 flex items-center gap-2">👤 Subscribers</h2>
        <div className="overflow-x-auto rounded-xl border border-gray-100 shadow-sm">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left text-sm font-semibold text-gray-600">Phone</th>
                <th className="px-4 py-2 text-left text-sm font-semibold text-gray-600">Language</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-100">
              {subs.length === 0 ? (
                <tr>
                  <td colSpan={2} className="px-4 py-6 text-center text-gray-400">No subscribers found.</td>
                </tr>
              ) : (
                subs.map((s) => (
                  <tr key={s.phone} className="hover:bg-gray-50 transition-colors">
                    <td className="px-4 py-3 text-gray-800">{s.phone}</td>
                    <td className="px-4 py-3 text-gray-800">{s.language}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
