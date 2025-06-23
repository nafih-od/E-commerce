from django.contrib import admin
from .models import Vendor, Product


class ProductInline(admin.TabularInline):  # Or use StackedInline if you prefer
    model = Product
    extra = 1
    fields = ('name', 'price', 'stock', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('license_number', 'store_name', 'user', 'contact_number', 'is_active', 'created_at')
    search_fields = ('store_name', 'user__username', 'contact_number')
    list_filter = ('is_active', 'created_at')
    inlines = [ProductInline]  # 🔥 This connects products inline with vendor
    ordering = ('store_name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'price', 'stock', 'created_at')
    search_fields = ('name', 'vendor__store_name')
    list_filter = ('vendor', 'created_at')
