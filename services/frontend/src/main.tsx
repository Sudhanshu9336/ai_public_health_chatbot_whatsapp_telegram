import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import './styles.css';
import Dashboard from './pages/Dashboard';
import Subscribers from './pages/Subscribers';
import Alerts from './pages/Alerts';

function AppShell() {
  return (
    <BrowserRouter>
      {/* Header */}
      <header className="bg-red-600 text-white p-4 flex items-center justify-between shadow-md">
        <h1 className="text-2xl font-bold">Odisha Public Health — Outreach</h1>
        <nav className="flex gap-6 text-sm font-medium">
          <Link
            to="/"
            className="hover:underline transition-colors duration-200"
          >
            Dashboard
          </Link>
          <Link
            to="/subscribers"
            className="hover:underline transition-colors duration-200"
          >
            Subscribers
          </Link>
          <Link
            to="/alerts"
            className="hover:underline transition-colors duration-200"
          >
            Broadcast
          </Link>
        </nav>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto p-6 space-y-6 min-h-[calc(100vh-128px)]">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/subscribers" element={<Subscribers />} />
          <Route path="/alerts" element={<Alerts />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="text-center text-gray-400 text-sm py-6 border-t">
        Built for PSID 25049 — AI-Driven Public Health Chatbot
      </footer>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(<AppShell />);
