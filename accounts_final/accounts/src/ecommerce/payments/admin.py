from django.contrib import admin
from .models import Order, OrderItem, DeliveryAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price_at_time', 'subtotal')

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = 'Subtotal'


class DeliveryAddressInline(admin.StackedInline):
    model = DeliveryAddress
    can_delete = False
    max_num = 1
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'placed_at', 'total_amount', 'razorpay_order_id', 'razorpay_payment_id')
    list_filter = ('placed_at',)
    search_fields = ('id', 'user__email', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('id', 'placed_at')
    inlines = [OrderItemInline, DeliveryAddressInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_at_time', 'subtotal')
    readonly_fields = ('subtotal',)
    search_fields = ('order__id', 'product__name')


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('order', 'full_name', 'city', 'state', 'zip_code', 'country', 'phone_number')
    search_fields = ('order__id', 'full_name', 'city', 'state')
