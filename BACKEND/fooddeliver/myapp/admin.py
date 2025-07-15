from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Payment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available']
    list_filter = ['category', 'available']
    search_fields = ['name', 'description']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ordered_at', 'status', 'total_amount']
    list_filter = ['status', 'ordered_at']
    search_fields = ['user__username', 'delivery_address']
    inlines = [OrderItemInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'method', 'payment_status', 'paid_at']
    list_filter = ['method', 'payment_status', 'paid_at']
    search_fields = ['order__user__username', 'transaction_id']
