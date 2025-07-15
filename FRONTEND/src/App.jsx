
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AdminLayout from './components/AdminLayout';
import Login from './pages/Login';
import AdminHome from './pages/home';
// ...existing code...
import Menu from './pages/admin/Menu';
import Orders from './pages/admin/Orders';
import ProtectedRoute from './components/ProtectedRoute';
import Header from './components/Header';
import Footer from './components/Footer';
import MenuPage from './pages/MenuPage';
import CartPage from './pages/CartPage';
import Dashboard from './pages/admin/Dashboard';


const App = () => {
  return (
    <Router>
      <Header />
      <main className="min-h-[80vh]">
        <Routes>
          <Route path="/login" element={<Login />} />
          {/* Landing page route - nice landing page */}
          <Route path="/" element={<AdminHome />} />
          <Route path="/menu" element={<MenuPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          {/* Admin Routes */}
          <Route path="/admin" element={<ProtectedRoute><AdminLayout /></ProtectedRoute>}>
            <Route index element={<Dashboard />} />
            <Route path="menu" element={<Menu />} />
            <Route path="orders" element={<Orders />} />
          </Route>
          {/* Redirect unknown routes to / */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
      <Footer />
    </Router>
  );
};

export default App;
