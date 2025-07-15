# Food Delivery System Backend

A Django REST Framework backend for a single-vendor food delivery system with JWT authentication and Khalti payment integration.

## Features

- JWT Authentication
- Menu Management
- Order Processing
- Payment Integration (Khalti)
- Admin Dashboard API
- Image Upload Support
- API Pagination

## API Endpoints

### Authentication
- `POST /auth/login/` - Obtain JWT token
- `POST /auth/refresh/` - Refresh JWT token

### Menu Management
- `GET /api/categories/` - List all categories
- `GET /api/products/` - List all products (supports pagination)
- `GET /api/products/?category={id}` - Filter products by category

### Orders
- `GET /api/orders/` - List user's orders (admins see all orders)
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details
- `POST /api/orders/{id}/update_status/` - Update order status (admin only)

### Payments
- `POST /api/payments/verify_khalti/` - Verify Khalti payment

## Setup Instructions

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure MySQL database in settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'food_delivery',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Start development server:
```bash
python manage.py runserver
```

## API Authentication

To access protected endpoints, include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Admin Access

Admin users can:
- Manage menu items
- View all orders
- Update order status
- Access payment information

## Media Files

Product images are stored in the `media/products/` directory. Make sure the directory has proper write permissions.

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error