import { useEffect, useState } from "react";

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/history")
      .then((res) => res.json())
      .then(setHistory)
      .catch(() => setHistory([]));
  }, []);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="max-w-4xl mx-auto bg-white shadow-2xl rounded-2xl p-6">
        <h2 className="text-2xl font-extrabold mb-6 flex items-center gap-2">📝 Broadcast History</h2>
        <ul className="space-y-4">
          {history.length === 0 ? (
            <p className="text-gray-500 text-center">No broadcast history yet.</p>
          ) : (
            history.map((h, i) => (
              <li
                key={i}
                className="p-4 border border-gray-100 rounded-2xl bg-white shadow hover:shadow-lg transition-shadow duration-300"
              >
                <p className="text-gray-800">{h.message}</p>
                <span className="text-sm text-gray-400 mt-2 block">
                  {new Date(h.timestamp).toLocaleString()}
                </span>
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}
