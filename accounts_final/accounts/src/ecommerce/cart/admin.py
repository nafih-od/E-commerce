from django.contrib import admin
from .models import Cart, CartItem, TempOrder, TempOrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username",)
    date_hierarchy = "created_at"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "added_at")
    search_fields = ("product__name", "cart__user__username")
    list_filter = ("added_at",)

class TempOrderItemInline(admin.TabularInline):
    model = TempOrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price_at_time', 'subtotal']
    can_delete = False


@admin.register(TempOrder)
class TempOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    inlines = [TempOrderItemInline]


@admin.register(TempOrderItem)
class TempOrderItemAdmin(admin.ModelAdmin):
    list_display = ['temp_order', 'product', 'quantity', 'price_at_time', 'subtotal']
    search_fields = ['product__name', 'temp_order__user__username']
    list_filter = ['product']