import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Main dashboard with nested routes */}
        <Route path="/*" element={<Dashboard />} />
        
        {/* Catch-all 404 page */}
        <Route path="404" element={<NotFound />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}
