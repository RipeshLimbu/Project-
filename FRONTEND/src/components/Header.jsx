import React from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';


import { useMemo } from 'react';

const Header = () => {
  const { isAuthenticated, user } = useSelector((state) => state.auth || {});
  // Use localStorage for cart
  const cart = useMemo(() => {
    return JSON.parse(localStorage.getItem('cart') || '[]');
  }, [localStorage.getItem('cart')]);
  const cartCount = useMemo(() => cart.reduce((sum, item) => sum + item.quantity, 0), [cart]);

  return (
    <header className="bg-white shadow sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="text-2xl font-bold text-indigo-600">FoodStore</Link>
        <nav className="flex items-center gap-6">
          <Link to="/" className="hover:text-indigo-700 font-medium">Home</Link>
          <Link to="/menu" className="hover:text-indigo-700 font-medium">Menu</Link>
          <Link to="/cart" className="relative hover:text-indigo-700 font-medium">
            Cart
            {cartCount > 0 && (
              <span className="absolute -top-2 -right-4 bg-indigo-600 text-white rounded-full px-2 text-xs">{cartCount}</span>
            )}
          </Link>
          {isAuthenticated ? (
            <Link to="/dashboard" className="hover:text-indigo-700 font-medium">Dashboard</Link>
          ) : (
            <Link to="/login" className="hover:text-indigo-700 font-medium">Login</Link>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;
