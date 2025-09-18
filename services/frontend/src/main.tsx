import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import './styles.css';
import Dashboard from './pages/Dashboard';
import Subscribers from './pages/Subscribers';
import Alerts from './pages/Alerts';

function Navigation() {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: '📊 Dashboard', icon: '🏠' },
    { path: '/subscribers', label: '👥 Subscribers', icon: '👤' },
    { path: '/alerts', label: '📢 Broadcast', icon: '📣' },
  ];

  return (
    <nav className="flex gap-6 text-sm font-medium">
      {navItems.map((item) => (
        <Link
          key={item.path}
          to={item.path}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 ${
            location.pathname === item.path
              ? 'bg-white/20 text-white font-semibold'
              : 'text-white/80 hover:text-white hover:bg-white/10'
          }`}
        >
          <span>{item.icon}</span>
          {item.label}
        </Link>
      ))}
    </nav>
  );
}

function AppShell() {
  return (
    <BrowserRouter>
      {/* Header */}
      <header className="bg-gradient-to-r from-red-600 to-red-700 text-white p-4 shadow-lg">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
              <span className="text-2xl">🏥</span>
            </div>
            <div>
              <h1 className="text-xl font-bold">Odisha Public Health</h1>
              <p className="text-sm text-white/80">AI-Driven Disease Awareness System</p>
            </div>
          </div>
          <Navigation />
        </div>
      </header>

      {/* Main content */}
      <main className="min-h-[calc(100vh-140px)] bg-gray-50">
        <div className="max-w-7xl mx-auto p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/subscribers" element={<Subscribers />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-6">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2 text-gray-600">
              <span className="text-green-600">●</span>
              <span className="text-sm">System Status: Operational</span>
            </div>
            <div className="text-center text-gray-500 text-sm">
              <p>Built for PSID 25049 — AI-Driven Public Health Chatbot</p>
              <p className="text-xs mt-1">Government of Odisha | Electronics & IT Department</p>
            </div>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span>v1.0.0</span>
              <span>•</span>
              <span>Last Updated: Jan 2025</span>
            </div>
          </div>
        </div>
      </footer>
    </BrowserRouter>
  );
}

function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
      <div className="text-6xl mb-4">🔍</div>
      <h2 className="text-2xl font-bold text-gray-800 mb-2">Page Not Found</h2>
      <p className="text-gray-600 mb-6">The page you're looking for doesn't exist.</p>
      <Link
        to="/"
        className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg transition-colors duration-200"
      >
        Go to Dashboard
      </Link>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AppShell />
  </React.StrictMode>
);