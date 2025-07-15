import React, { useEffect, useState } from 'react';
import api from '../services/api';

const CartItem = ({ item, onUpdate, onRemove }) => {
  const [quantity, setQuantity] = useState(item.quantity);

  const handleUpdate = (newQty) => {
    setQuantity(newQty);
    onUpdate(item.id, newQty);
  };

  return (
    <div className="flex items-center justify-between bg-white rounded-xl shadow-lg p-4 mb-4 hover:shadow-2xl transition">
      <div className="flex items-center gap-4">
        {item.image ? (
          <img src={item.image} alt={item.name} className="h-20 w-20 object-cover rounded-lg" />
        ) : (
          <div className="h-20 w-20 bg-gray-200 flex items-center justify-center rounded-lg text-gray-400">No Image</div>
        )}
        <div>
          <div className="font-semibold text-lg">{item.name}</div>
          <div className="text-gray-500">₹{item.price}</div>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <button onClick={() => handleUpdate(quantity - 1)} disabled={quantity <= 1} className="px-3 py-1 bg-gray-200 rounded-lg font-bold text-lg">-</button>
        <span className="px-2 font-semibold">{quantity}</span>
        <button onClick={() => handleUpdate(quantity + 1)} className="px-3 py-1 bg-gray-200 rounded-lg font-bold text-lg">+</button>
      </div>
      <button onClick={() => onRemove(item.id)} className="text-red-600 hover:underline ml-4 font-medium">Remove</button>
    </div>
  );
};

const CartPage = () => {
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = window.reactRouterNavigate || ((path) => { window.location.href = path });

  useEffect(() => {
    setCart(api.cart.get());
    setLoading(false);
  }, []);

  const handleUpdate = (id, quantity) => {
    api.cart.update(id, Math.max(1, quantity));
    setCart(api.cart.get());
  };

  const handleRemove = (id) => {
    api.cart.remove(id);
    setCart(api.cart.get());
  };

  const handleCheckout = async () => {
    try {
      setLoading(true);
      const orderItems = cart.map(item => ({ product: item.id, quantity: item.quantity, price: item.price }));
      const payload = {
        items: orderItems,
        delivery_address: 'Test Address',
        special_instructions: '',
      };
      // Do NOT send 'user' field, backend will use JWT user
      const res = await api.order.place(payload);
      api.cart.clear();
      setCart([]);
      setLoading(false);
      window.location.href = '/';
    } catch (err) {
      if (err.response && err.response.status === 401) {
        // Unauthorized, redirect to login
        navigate('/login');
      } else {
        setError('Checkout failed.');
      }
      setLoading(false);
    }
  };

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  if (loading) return <div className="flex justify-center items-center min-h-screen">Loading cart...</div>;
  if (error) return <div className="flex justify-center items-center min-h-screen text-red-500">{error}</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-10">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8 text-center">Your Cart</h1>
        {cart.length === 0 ? (
          <div className="text-center text-gray-500">Your cart is empty.</div>
        ) : (
          <>
            {cart.map(item => (
              <CartItem key={item.id} item={item} onUpdate={handleUpdate} onRemove={handleRemove} />
            ))}
            <div className="flex justify-between items-center mt-8 p-4 bg-white rounded-xl shadow">
              <span className="text-2xl font-bold text-indigo-700">Total: ₹{total}</span>
              <button onClick={handleCheckout} className="bg-indigo-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition shadow">Proceed to Checkout</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default CartPage;
