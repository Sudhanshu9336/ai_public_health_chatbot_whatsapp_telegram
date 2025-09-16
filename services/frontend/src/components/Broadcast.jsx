import { useState } from "react";

export default function Broadcast() {
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState("");

  const sendBroadcast = async () => {
    try {
      const res = await fetch("http://localhost:8000/broadcast", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      setStatus({ type: "success", text: `✅ Sent to ${data.recipients} subscribers` });
    } catch (err) {
      setStatus({ type: "error", text: "❌ Failed to send alert" });
    }
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen flex flex-col items-center justify-center">
      <div className="w-full max-w-xl bg-white shadow-2xl rounded-2xl p-8 space-y-6 border-t-8 border-red-600">
        <h2 className="text-2xl font-extrabold text-gray-800 flex items-center gap-2">
          📢 Broadcast Alert
        </h2>
        <p className="text-gray-500">
          Send important health alerts to all your subscribers instantly.
        </p>

        <textarea
          className="w-full border border-gray-300 rounded-xl p-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-transparent resize-none transition-all duration-300"
          rows="5"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your health alert message here..."
        />

        <button
          onClick={sendBroadcast}
          className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-xl shadow-lg transition-transform transform hover:-translate-y-1 active:translate-y-0"
        >
          Send Alert
        </button>

        {status && (
          <div
            className={`mt-4 p-3 rounded-lg font-medium ${
              status.type === "success"
                ? "bg-green-100 text-green-700 border border-green-200"
                : "bg-red-100 text-red-700 border border-red-200"
            } animate-fadeIn`}
          >
            {status.text}
          </div>
        )}
      </div>
    </div>
  );
}
