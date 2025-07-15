from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
import requests
import json

from .models import Category, Product, Order, OrderItem, Payment, UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, CategorySerializer,
    ProductSerializer, OrderSerializer, OrderItemSerializer, PaymentSerializer
)

class IsAdminUser(IsAdminUser):
    pass

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'verify_token']:
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def profile(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        user = request.user
        profile = user.userprofile

        # Update User model fields
        user_serializer = self.get_serializer(user, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # Update UserProfile model fields
        profile_data = request.data.get('profile', {})
        profile_serializer = UserProfileSerializer(profile, data=profile_data, partial=True)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        return Response(user_serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=True)
    def products(self, request, pk=None):
        category = self.get_object()
        products = category.product_set.filter(available=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category__name', 'ingredients']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured', 'search']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        is_vegetarian = self.request.query_params.get('vegetarian', None)
        is_spicy = self.request.query_params.get('spicy', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if category:
            queryset = queryset.filter(category__id=category)
        if is_vegetarian:
            queryset = queryset.filter(is_vegetarian=is_vegetarian.lower() == 'true')
        if is_spicy:
            queryset = queryset.filter(is_spicy=is_spicy.lower() == 'true')
        if min_price:
            queryset = queryset.filter(current_price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(current_price__lte=float(max_price))

        return queryset.filter(available=True)

    @action(detail=False)
    def featured(self, request):
        featured_products = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def search(self, request):
        search_term = request.data.get('search', '')
        products = self.get_queryset().filter(
            Q(name__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(ingredients__icontains=search_term)
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart_items = self.request.data.get('items', [])
        total_amount = 0
        order = serializer.save(user=self.request.user, total_amount=0)  # temp value
        for item in cart_items:
            product = Product.objects.get(id=item['product'])
            quantity = item['quantity']
            special_instructions = item.get('special_instructions', '')
            price = float(product.current_price)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                special_instructions=special_instructions
            )
            total_amount += price * quantity
        order.total_amount = total_amount
        order.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You don't have permission to cancel this order."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if order.status not in ['Pending', 'Confirmed']:
            return Response(
                {"detail": "This order cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'Cancelled'
        order.save()
        return Response({"detail": "Order cancelled successfully."})

    @action(detail=False)
    def history(self, request):
        orders = self.get_queryset().order_by('-created_at')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def active(self, request):
        active_statuses = ['Pending', 'Confirmed', 'Preparing', 'On the Way']
        orders = self.get_queryset().filter(status__in=active_statuses).order_by('-created_at')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(order__user=self.request.user)

    @action(detail=False, methods=['post'])
    def verify_khalti(self, request):
        token = request.data.get('token')
        amount = request.data.get('amount')
        order_id = request.data.get('order_id')

        if not all([token, amount, order_id]):
            return Response(
                {"detail": "Missing required parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verify with Khalti API
        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                # Create payment record
                payment = Payment.objects.create(
                    order=order,
                    method='khalti',
                    amount=amount/100,  # Convert paisa to rupees
                    transaction_id=response_data['idx'],
                    payment_status='completed',
                    payment_response=response_data,
                    paid_at=timezone.now()
                )

                # Update order status
                order.status = 'Confirmed'
                order.save()

                return Response({
                    "detail": "Payment verified successfully.",
                    "payment": PaymentSerializer(payment).data
                })
            else:
                return Response(
                    {"detail": "Payment verification failed.", "errors": response_data},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except requests.exceptions.RequestException as e:
            return Response(
                {"detail": "Error connecting to payment gateway.", "errors": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=False)
    def history(self, request):
        payments = self.get_queryset().order_by('-created_at')
        page = self.paginate_queryset(payments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)
