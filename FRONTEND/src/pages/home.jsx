import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import delivery1 from '../assets/delivery1.jpg';
import { FaUtensils, FaShippingFast, FaClock, FaHeart } from 'react-icons/fa';

const LandingPage = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative h-[70vh] bg-gradient-to-r from-indigo-600 to-purple-600">
        <div className="absolute inset-0">
          <img src={delivery1} alt="Hero" className="w-full h-full object-cover opacity-20" />
        </div>
        <div className="relative max-w-7xl mx-auto px-4 h-full flex items-center">
          <div className="text-white">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Delicious Food,
              <br />
              <span className="text-yellow-400">Delivered Fast</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 max-w-2xl">
              Experience the finest cuisine from our kitchen to your doorstep. 
              Fresh, fast, and always delicious.
            </p>
            <Link to="/menu" className="bg-yellow-400 text-gray-900 px-8 py-3 rounded-full text-lg font-semibold hover:bg-yellow-300 transition duration-300 inline-block">
              Order Now
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">Why Choose Us?</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center p-6 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-300">
              <div className="text-4xl text-indigo-600 mb-4 flex justify-center">
                <FaUtensils />
              </div>
              <h3 className="text-xl font-semibold mb-2">Quality Food</h3>
              <p className="text-gray-600">Fresh ingredients and expert chefs</p>
            </div>
            <div className="text-center p-6 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-300">
              <div className="text-4xl text-indigo-600 mb-4 flex justify-center">
                <FaShippingFast />
              </div>
              <h3 className="text-xl font-semibold mb-2">Fast Delivery</h3>
              <p className="text-gray-600">Quick and reliable service</p>
            </div>
            <div className="text-center p-6 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-300">
              <div className="text-4xl text-indigo-600 mb-4 flex justify-center">
                <FaClock />
              </div>
              <h3 className="text-xl font-semibold mb-2">24/7 Service</h3>
              <p className="text-gray-600">Available whenever you need</p>
            </div>
            <div className="text-center p-6 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-300">
              <div className="text-4xl text-indigo-600 mb-4 flex justify-center">
                <FaHeart />
              </div>
              <h3 className="text-xl font-semibold mb-2">Best Quality</h3>
              <p className="text-gray-600">Satisfaction guaranteed</p>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action Section */}
      <div className="py-16 bg-gradient-to-r from-purple-600 to-indigo-600 text-white">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Order?</h2>
          <p className="text-xl mb-8">Start your delicious journey with us today!</p>
          <Link to="/menu" className="bg-white text-indigo-600 px-8 py-3 rounded-full text-lg font-semibold hover:bg-gray-100 transition duration-300 inline-block">
            View Menu
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
