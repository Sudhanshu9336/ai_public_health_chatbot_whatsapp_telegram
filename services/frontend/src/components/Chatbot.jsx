import { useState, useRef, useEffect } from "react";

export default function Chatbot() {
  setMessages(prev => [...prev, { from: "bot", text: "This is a bot message" }]);

  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { from: "user", text: input }]);

    const res = await fetch("http://localhost:5005/webhooks/rest/webhook", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender: "user", message: input }),
    });

    const data = await res.json();
    if (data && data.length > 0) {
      setMessages((prev) => [...prev, { from: "bot", text: data[0].text }]);
    }
    setInput("");
  };

  // Auto-scroll to bottom
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="p-6 bg-gray-50 min-h-screen flex flex-col items-center justify-center">
      <div className="w-full max-w-2xl bg-white shadow-2xl rounded-3xl p-6 flex flex-col h-[600px]">
        <h2 className="text-2xl font-extrabold text-gray-800 mb-4 flex items-center gap-2">
          💬 Health Chatbot
        </h2>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 bg-gray-100 rounded-3xl mb-4 space-y-3 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
          {messages.length === 0 && (
            <p className="text-gray-400 text-center mt-10">Start chatting with the Health Bot...</p>
          )}
          {messages.map((m, i) => (
            <div
              key={i}
              className={`flex ${m.from === "user" ? "justify-end" : "justify-start"}`}
            >
              <span
                className={`inline-block max-w-[70%] px-4 py-2 rounded-2xl break-words ${
                  m.from === "user"
                    ? "bg-red-600 text-white rounded-br-none shadow"
                    : "bg-white text-gray-800 shadow rounded-bl-none"
                }`}
              >
                {m.text}
              </span>
            </div>
          ))}
          <div ref={scrollRef}></div>
        </div>

        {/* Input */}
        <div className="flex gap-2">
          <input
            className="flex-1 border border-gray-300 rounded-2xl px-4 py-2 focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-transparent transition-all duration-200"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about health topics..."
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button
            onClick={sendMessage}
            className="bg-red-600 hover:bg-red-700 text-white font-bold px-6 py-2 rounded-2xl shadow-lg transition-transform transform hover:-translate-y-1 active:translate-y-0"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
