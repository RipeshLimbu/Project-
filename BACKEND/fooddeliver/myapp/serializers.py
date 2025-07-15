from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, Order, OrderItem, Payment, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'address', 'created_at', 'updated_at')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(source='userprofile', read_only=True)
    is_admin = serializers.BooleanField(required=False, write_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'profile', 'full_name', 'date_joined')
        read_only_fields = ('date_joined',)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def create(self, validated_data):
        is_admin = validated_data.pop('is_admin', False)
        user = User.objects.create_user(**validated_data)
        user.is_staff = is_admin
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'product_count')

    def get_product_count(self, obj):
        return obj.product_set.count()

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'category', 'category_name', 'price',
            'discount_price', 'current_price', 'discount_percentage', 'image',
            'available', 'is_vegetarian', 'is_spicy', 'preparation_time',
            'calories', 'ingredients', 'is_featured', 'created_at', 'updated_at'
        )

    def get_discount_percentage(self, obj):
        if obj.discount_price and obj.price:
            discount = ((obj.price - obj.discount_price) / obj.price) * 100
            return round(discount, 2)
        return 0

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.current_price', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            'id', 'order', 'product', 'product_name', 'product_price',
            'quantity', 'special_instructions', 'subtotal',
            'created_at', 'updated_at'
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'user_name', 'items', 'status', 'status_display',
            'total_amount', 'delivery_address', 'special_instructions',
            'estimated_delivery_time', 'delivery_notes', 'payment_status',
            'created_at', 'updated_at'
        )
        read_only_fields = ('total_amount', 'payment_status')

    def get_payment_status(self, obj):
        try:
            return obj.payment.payment_status
        except Payment.DoesNotExist:
            return 'pending'

class PaymentSerializer(serializers.ModelSerializer):
    order_details = OrderSerializer(source='order', read_only=True)
    payment_method_display = serializers.CharField(source='get_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id', 'order', 'order_details', 'method', 'payment_method_display',
            'amount', 'transaction_id', 'payment_status', 'payment_response',
            'paid_at', 'created_at', 'updated_at'
        )
        read_only_fields = ('payment_response', 'paid_at', 'created_at', 'updated_at')