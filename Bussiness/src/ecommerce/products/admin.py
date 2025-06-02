from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Adjust the number of extra forms as nee


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('name', 'product_type', 'price', 'brand', 'stock_quantity', 'created_at')

    # Allow filtering based on product_type, brand, and date added
    list_filter = ('product_type', 'brand', 'created_at')

    # Enable search by name, description, brand, or category
    search_fields = ('name', 'description', 'brand', 'category')

    inlines = [ProductImageInline]  # This adds the inline to the admin

    # Group fields into sections for better organization
    fieldsets = (
        ("Base Information", {
            'fields': ('product_type', 'name', 'description', 'price', 'brand', 'category', 'stock_quantity')
        }),
        ("TV Details", {
            'classes': ('collapse',),
            'fields': (
                'screen_size', 'resolution', 'panel_type', 'smart_tv',
                'hdmi_ports', 'usb_ports', 'refresh_rate', 'operating_system', 'tv_energy_rating'
            ),
        }),
        ("Speaker Details", {
            'classes': ('collapse',),
            'fields': (
                'speaker_type', 'connectivity', 'power_source', 'frequency_range',
                'weight', 'speaker_features', 'speaker_release_date', 'speaker_image'
            ),
        }),
        ("Refrigerator Details", {
            'classes': ('collapse',),
            'fields': (
                'capacity', 'door_style', 'refrigerator_energy_rating',
                'has_water_dispenser', 'has_ice_maker', 'refrigerator_image'
            ),
        }),
        ("AC Details", {
            'classes': ('collapse',),
            'fields': (
                'ac_type', 'ac_capacity', 'ac_energy_rating', 'ac_features',
                'noise_level', 'ac_release_date', 'ac_image'
            ),
        }),
    )