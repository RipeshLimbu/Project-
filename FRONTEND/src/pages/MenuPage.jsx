
import React, { useEffect, useState } from 'react';
import api from '../services/api';

const MenuPage = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.menu.getAll()
      .then(res => {
        if (Array.isArray(res.data)) {
          setItems(res.data);
        } else if (Array.isArray(res.data.results)) {
          setItems(res.data.results);
        } else {
          setItems([]);
        }
        setLoading(false);
      })
      .catch(err => {
        setError('Failed to load menu.');
        setLoading(false);
      });
  }, []);

  const handleAddToCart = (item) => {
    api.cart.add({
      id: item.id,
      name: item.name,
      price: item.price,
      image: item.image,
      quantity: 1
    });
    alert('Added to cart!');
  };

  if (loading) return <div className="flex justify-center items-center min-h-screen">Loading menu...</div>;
  if (error) return <div className="flex justify-center items-center min-h-screen text-red-500">{error}</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-10">
      <div className="max-w-5xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8 text-center">Menu</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
          {items.map(item => (
            <div key={item.id} className="bg-white rounded-xl shadow-lg p-4 flex flex-col hover:shadow-2xl transition">
              <div className="relative">
                {item.image ? (
                  <img src={item.image} alt={item.name} className="h-48 w-full object-cover rounded-lg mb-4" />
                ) : (
                  <div className="h-48 w-full bg-gray-200 flex items-center justify-center rounded-lg mb-4 text-gray-400">No Image</div>
                )}
                {item.is_featured && (
                  <span className="absolute top-2 left-2 bg-yellow-400 text-xs font-bold px-2 py-1 rounded">Featured</span>
                )}
              </div>
              <h2 className="text-lg font-bold mb-1 text-gray-900">{item.name}</h2>
              <p className="text-gray-500 mb-2 text-sm">{item.description}</p>
              <div className="flex items-center justify-between mt-auto">
                <span className="text-xl font-bold text-indigo-600">₹{item.price}</span>
                <button
                  className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-indigo-700 transition shadow"
                  onClick={() => handleAddToCart(item)}
                >
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MenuPage;
