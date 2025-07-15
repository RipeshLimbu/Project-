import React from 'react';

const AdminHome = () => (
  <div className="max-w-3xl mx-auto py-12 px-4">
    <h1 className="text-3xl font-bold mb-4 text-indigo-700">Admin Dashboard Home</h1>
    <p className="text-lg text-gray-700 mb-8">
      Welcome to the FoodStore Admin Dashboard. Here you can manage products, view orders, track revenue, and oversee customer activity. Use the navigation to access different admin features and monitor your business performance.
    </p>
    <div className="bg-indigo-50 rounded-lg p-6 shadow">
      <h2 className="text-xl font-semibold mb-2">Quick Overview</h2>
      <ul className="list-disc pl-6 text-gray-600">
        <li>Manage menu items and prices</li>
        <li>View and process customer orders</li>
        <li>Track total revenue and sales stats</li>
        <li>Access customer profiles and feedback</li>
      </ul>
    </div>
  </div>
);

export default AdminHome;
