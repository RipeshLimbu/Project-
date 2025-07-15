import React from 'react';
import { FaFacebookF, FaTwitter, FaInstagram, FaLinkedinIn } from 'react-icons/fa';

const Footer = () => (
  <footer className="bg-gray-900 py-6 mt-12 border-t border-gray-700">
         <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-8 text-sm">

        {/* Company */}
        <div>
          <h4 className="font-semibold text-lg border-b-2 border-pink-500 inline-block mb-3">Company</h4>
          <ul className="space-y-2 text-gray-400">
            <li><a href="#">About Us</a></li>
            <li><a href="#">Our Services</a></li>
            <li><a href="#">Privacy Policy</a></li>
            <li><a href="#">Affiliate Program</a></li>
          </ul>
        </div>

        {/* Get Help */}
        <div>
          <h4 className="font-semibold text-lg border-b-2 border-pink-500 inline-block mb-3">Get Help</h4>
          <ul className="space-y-2 text-gray-400">
            <li><a href="#">FAQ</a></li>
            <li><a href="#">Shipping</a></li>
            <li><a href="#">Returns</a></li>
            <li><a href="#">Order Status</a></li>
            <li><a href="#">Payment Options</a></li>
          </ul>
        </div>

        {/* Online Shop */}
        <div>
          <h4 className="font-semibold text-lg border-b-2 border-pink-500 inline-block mb-3">Online Shop</h4>
          <ul className="space-y-2 text-gray-400">
            <li><a href="#">Watch</a></li>
            <li><a href="#">Bag</a></li>
            <li><a href="#">Shoes</a></li>
            <li><a href="#">Dress</a></li>
          </ul>
        </div>

        {/* Follow Us */}
        <div>
          <h4 className="font-semibold text-lg border-b-2 border-pink-500 inline-block mb-3">Follow Us</h4>
          <div className="flex space-x-4 mt-4 text-lg text-gray-400">
            <a href="#" className="hover:text-white"><FaFacebookF /></a>
            <a href="#" className="hover:text-white"><FaTwitter /></a>
            <a href="#" className="hover:text-white"><FaInstagram /></a>
            <a href="#" className="hover:text-white"><FaLinkedinIn /></a>
          </div>
        </div>

      </div>
  </footer>
);

export default Footer;
    