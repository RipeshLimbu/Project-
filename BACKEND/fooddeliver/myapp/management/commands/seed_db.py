import os
import random
import requests
import json
from decimal import Decimal
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from myapp.models import Category, Product, Order, OrderItem, Payment

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def download_image(self, url, filename):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile()  # Remove delete=True for compatibility
                img_temp.write(response.content)
                img_temp.flush()
                return File(img_temp), True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error downloading image: {str(e)}'))
        return None, False

    def handle(self, *args, **kwargs):
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            email='admin@example.com',
            is_staff=True,
            is_superuser=True
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create regular users
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                email=f'user{i}@example.com'
            )
            if created:
                user.set_password('user123')
                user.save()
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created/Retrieved user{i}'))

        # Create categories
        categories = [
            'Breakfast',
            'Lunch',
            'Dinner',
            'Snacks',
            'Beverages'
        ]
        category_objects = []
        for cat_name in categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            category_objects.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))

        # Sample food items with Pexels image URLs
        food_items = [
            # Breakfast Items
            {
                'name': 'English Breakfast',
                'category': 'Breakfast',
                'description': 'Classic English breakfast with eggs, bacon, beans, and toast',
                'price': 15.99,
                'image_url': 'https://images.pexels.com/photos/139746/pexels-photo-139746.jpeg',
                'is_vegetarian': False,
                'preparation_time': 20,
                'calories': 850,
                'ingredients': 'Eggs, bacon, beans, toast, mushrooms, tomatoes',
                'is_featured': True
            },
            {
                'name': 'Pancake Stack',
                'category': 'Breakfast',
                'description': 'Fluffy pancakes served with maple syrup and fresh berries',
                'price': 12.99,
                'image_url': 'https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg',
                'is_vegetarian': True,
                'preparation_time': 15,
                'calories': 550,
                'ingredients': 'Flour, eggs, milk, butter, maple syrup, mixed berries',
                'discount_price': 10.99
            },
            # Lunch Items
            {
                'name': 'Classic Burger',
                'category': 'Lunch',
                'description': 'Juicy beef patty with fresh vegetables and special sauce',
                'price': 14.99,
                'image_url': 'https://images.pexels.com/photos/1639557/pexels-photo-1639557.jpeg',
                'is_vegetarian': False,
                'preparation_time': 25,
                'calories': 750,
                'ingredients': 'Beef patty, lettuce, tomato, onion, cheese, special sauce',
                'is_spicy': False
            },
            {
                'name': 'Chicken Caesar Salad',
                'category': 'Lunch',
                'description': 'Fresh romaine lettuce with grilled chicken and Caesar dressing',
                'price': 13.99,
                'image_url': 'https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg',
                'is_vegetarian': False,
                'preparation_time': 15,
                'calories': 450,
                'ingredients': 'Romaine lettuce, grilled chicken, parmesan, croutons, Caesar dressing'
            },
            # Dinner Items
            {
                'name': 'Margherita Pizza',
                'category': 'Dinner',
                'description': 'Traditional Italian pizza with fresh mozzarella and basil',
                'price': 18.99,
                'image_url': 'https://images.pexels.com/photos/825661/pexels-photo-825661.jpeg',
                'is_vegetarian': True,
                'preparation_time': 30,
                'calories': 800,
                'ingredients': 'Pizza dough, tomato sauce, fresh mozzarella, basil, olive oil',
                'is_featured': True
            },
            {
                'name': 'Spicy Thai Curry',
                'category': 'Dinner',
                'description': 'Rich and spicy Thai red curry with vegetables',
                'price': 16.99,
                'image_url': 'https://images.pexels.com/photos/699953/pexels-photo-699953.jpeg',
                'is_vegetarian': True,
                'preparation_time': 35,
                'calories': 600,
                'ingredients': 'Coconut milk, Thai red curry paste, tofu, mixed vegetables, rice',
                'is_spicy': True
            },
            # Snacks
            {
                'name': 'French Fries',
                'category': 'Snacks',
                'description': 'Crispy golden fries with special seasoning',
                'price': 6.99,
                'image_url': 'https://images.pexels.com/photos/1583884/pexels-photo-1583884.jpeg',
                'is_vegetarian': True,
                'preparation_time': 15,
                'calories': 350,
                'ingredients': 'Potatoes, vegetable oil, salt, special seasoning',
                'discount_price': 5.99
            },
            # Beverages
            {
                'name': 'Fresh Fruit Smoothie',
                'category': 'Beverages',
                'description': 'Blend of seasonal fruits with yogurt',
                'price': 7.99,
                'image_url': 'https://images.pexels.com/photos/434295/pexels-photo-434295.jpeg',
                'is_vegetarian': True,
                'preparation_time': 10,
                'calories': 200,
                'ingredients': 'Mixed fruits, yogurt, honey, ice'
            }
        ]

        # Create products
        for item in food_items:
            category = next(cat for cat in category_objects if cat.name == item['category'])
            try:
                product = Product.objects.get(name=item['name'])
                self.stdout.write(self.style.WARNING(f'Product {item["name"]} already exists, updating...'))
            except Product.DoesNotExist:
                product = Product(name=item['name'])
                self.stdout.write(self.style.SUCCESS(f'Creating new product: {item["name"]}'))

            # Update all fields
            product.category = category
            product.description = item['description']
            product.price = item['price']
            product.available = True
            product.is_vegetarian = item.get('is_vegetarian', False)
            product.is_spicy = item.get('is_spicy', False)
            product.preparation_time = item.get('preparation_time', 30)
            product.calories = item.get('calories')
            product.ingredients = item.get('ingredients', '')
            product.is_featured = item.get('is_featured', False)
            product.discount_price = item.get('discount_price')

            # Handle image download and save
            if not product.image or not product.image.name:
                image_file, success = self.download_image(
                    item['image_url'],
                    f"{item['name'].lower().replace(' ', '_')}.jpg"
                )
                if success:
                    product.image.save(
                        f"{item['name'].lower().replace(' ', '_')}.jpg",
                        image_file,
                        save=True
                    )
                    self.stdout.write(self.style.SUCCESS(f'Added image for: {item["name"]}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Failed to download image for: {item["name"]}'))

            product.save()

        # Create orders and payments
        products = Product.objects.all()
        start_date = datetime.now() - timedelta(weeks=3)

        for _ in range(20):  # Create 20 orders
            user = random.choice(users)
            order_date = start_date + timedelta(
                days=random.randint(0, 21),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            order = Order.objects.create(
                user=user,
                ordered_at=order_date,
                status=random.choice(['Delivered', 'Preparing', 'On the Way', 'Cancelled']),
                total_amount=0,
                delivery_address=f'{random.randint(1, 999)} Sample Street, City'
            )

            # Add 1-4 items to each order
            total_amount = 0
            for _ in range(random.randint(1, 4)):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                price = product.price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total_amount += price * quantity

            order.total_amount = total_amount
            order.save()

            # Create payment for completed orders
            if order.status in ['Delivered', 'Preparing', 'On the Way']:
                payment_method = random.choice(['khalti', 'esewa', 'cod'])
                payment_status = 'completed' if order.status == 'Delivered' else 'processing'
                
                # Simulate payment gateway response
                payment_response = {
                    'transaction_id': f'TRANS_{order.id}_{random.randint(1000, 9999)}',
                    'gateway': payment_method,
                    'status': payment_status,
                    'amount': total_amount,
                    'currency': 'NPR',
                    'created_at': order_date.isoformat()
                }
                
                if payment_method == 'khalti':
                    payment_response.update({
                        'idx': f'KHALTI_{random.randint(10000, 99999)}',
                        'token': f'KHALTI_TOKEN_{random.randint(100000, 999999)}',
                        'type': 'wallet'
                    })
                
                Payment.objects.create(
                    order=order,
                    method=payment_method,
                    amount=total_amount,
                    transaction_id=payment_response['transaction_id'],
                    payment_status=payment_status,
                    payment_response=json.loads(json.dumps(payment_response, cls=DecimalEncoder)),
                    paid_at=order_date
                )

            self.stdout.write(self.style.SUCCESS(f'Created order #{order.id} for {user.username}'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))