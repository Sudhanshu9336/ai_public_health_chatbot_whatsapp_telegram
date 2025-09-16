import { Link, useLocation } from 'react-router-dom';

const menu = [
  { name: '🏠 Dashboard', path: '/' },
  { name: '📢 Broadcast', path: '/broadcasts' },
  { name: '👤 Subscribers', path: '/subscribers' },
  { name: '💬 Chatbot', path: '/chatbot' },
  { name: '📝 History', path: '/history' },
  { name: '⚠️ Alerts', path: '/alerts' },
];

export default function Sidebar() {
  const { pathname } = useLocation();
  return (
    <aside className="w-64 bg-white shadow-md flex flex-col h-screen">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-blue-600">Health Dashboard</h1>
      </div>
      <nav className="flex-1 mt-6">
        {menu.map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={`block px-6 py-3 rounded hover:bg-blue-50 font-medium ${
              pathname === item.path ? 'bg-blue-100 text-blue-600' : 'text-gray-700'
            }`}
          >
            {item.name}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
