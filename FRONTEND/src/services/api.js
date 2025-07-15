import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000'; // Update if your backend runs elsewhere

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // Log request
    console.log('[API REQUEST]', config.method?.toUpperCase(), config.url, config.data || '');
    return config;
  },
  (error) => {
    console.error('[API REQUEST ERROR]', error);
    return Promise.reject(error);
  }
);

// Global response interceptor for 401 Unauthorized
api.interceptors.response.use(
  (response) => {
    // Log response
    console.log('[API RESPONSE]', response.config?.url, response.status, response.data);
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // Redirect to login page
      window.location.href = '/login';
    }
    console.error('[API RESPONSE ERROR]', error.config?.url, error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// --- AUTH ---
const auth = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (data) => api.post('/api/register/', data),
  getUser: () => api.get('/api/user/'),
  logout: () => api.post('/api/logout/'),
};

// --- CUSTOMER ---
const menu = {
  getAll: () => api.get('/api/products/'),
};



const order = {
  place: (data) => api.post('/api/orders/', data),
  getAll: () => api.get('/api/orders/'),
  getOne: (id) => api.get(`/api/orders/${id}/`),
};

const payment = {
  verify: (data) => api.post('/api/payment/verify/', data),
};

// --- ADMIN ---
const admin = {
  summary: () => api.get('/api/admin/summary/'),
  orders: {
    getAll: () => api.get('/api/admin/orders/'),
    getOne: (id) => api.get(`/api/admin/orders/${id}/`),
    updateStatus: (id, data) => api.patch(`/api/admin/orders/${id}/status/`, data),
  },
  menu: {
    getAll: () => api.get('/api/admin/menu/'),
    add: (data) => api.post('/api/admin/menu/', data),
    edit: (id, data) => api.put(`/api/admin/menu/${id}/`, data),
    remove: (id) => api.delete(`/api/admin/menu/${id}/`),
  },
};


// LocalStorage-based cart logic
const cart = {
  get: () => {
    return JSON.parse(localStorage.getItem('cart') || '[]');
  },
  add: (item) => {
    const cartItems = cart.get();
    const existing = cartItems.find(i => i.id === item.id);
    if (existing) {
      existing.quantity += item.quantity;
    } else {
      cartItems.push(item);
    }
    localStorage.setItem('cart', JSON.stringify(cartItems));
  },
  update: (id, quantity) => {
    const cartItems = cart.get().map(i => i.id === id ? { ...i, quantity } : i);
    localStorage.setItem('cart', JSON.stringify(cartItems));
  },
  remove: (id) => {
    const cartItems = cart.get().filter(i => i.id !== id);
    localStorage.setItem('cart', JSON.stringify(cartItems));
  },
  clear: () => {
    localStorage.removeItem('cart');
  }
};

export default {
  auth,
  menu,
  cart,
  order,
  payment,
  admin,
};