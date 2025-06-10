# from django.contrib import admin
# from .models import Product, ProductImage
#
#
# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 3  # Adjust the number of extra forms as nee
#
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     # Fields to display in the list view
#     list_display = ('name', 'product_type', 'price', 'brand', 'stock_quantity', 'created_at')
#
#     # Allow filtering based on product_type, brand, and date added
#     list_filter = ('product_type', 'brand', 'created_at')
#
#     # Enable search by name, description, brand, or category
#     search_fields = ('name', 'description', 'brand', 'category')
#
#     inlines = [ProductImageInline]  # This adds the inline to the admin
#
#     # Group fields into sections for better organization
#     fieldsets = (
#         ("Base Information", {
#             'fields': ('product_type', 'name', 'description', 'price', 'brand', 'category', 'stock_quantity')
#         }),
#         ("TV Details", {
#             'classes': ('collapse',),
#             'fields': (
#                 'screen_size', 'resolution', 'panel_type', 'smart_tv',
#                 'hdmi_ports', 'usb_ports', 'refresh_rate', 'operating_system', 'tv_energy_rating'
#             ),
#         }),
#         ("Speaker Details", {
#             'classes': ('collapse',),
#             'fields': (
#                 'speaker_type', 'connectivity', 'power_source', 'frequency_range',
#                 'weight', 'speaker_features', 'speaker_release_date', 'speaker_image'
#             ),
#         }),
#         ("Refrigerator Details", {
#             'classes': ('collapse',),
#             'fields': (
#                 'capacity', 'door_style', 'refrigerator_energy_rating',
#                 'has_water_dispenser', 'has_ice_maker', 'refrigerator_image'
#             ),
#         }),
#         ("AC Details", {
#             'classes': ('collapse',),
#             'fields': (
#                 'ac_type', 'ac_capacity', 'ac_energy_rating', 'ac_features',
#                 'noise_level', 'ac_release_date', 'ac_image'
#             ),
#         }),
#     )



from django.contrib import admin
from django.db import models
from django.forms import widgets
from .models import Product, ProductImage, Product_type


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'caption')
    verbose_name = "Product Image"
    verbose_name_plural = "Product Images"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'price',
        'stock_quantity',
        'release_date',
        'updated_at',
        'product_type',
    )
    list_filter = ('product_type','brand', 'category')
    search_fields = ('name', 'brand', 'category')
    inlines = [ProductImageInline]

    fieldsets = (
        ('General Information', {
            'fields': (
                'name',
                'description',
                'product_type',
                'brand',
                'category',
                'price',
                'stock_quantity',
                'release_date',
            )
        }),
        ('dynamic_properties', {
            'classes': ('collapse',),
            'fields': ('dynamic_properties',),
            'description': 'Store product-specific attributes in JSON format. For example, a TV can store its screen '
                           'size, resolution, etc.'
        }),
    )

    # Override the widget for JSONField to make it more user-friendly in the admin panel.
    formfield_overrides = {
        models.JSONField: {'widget': widgets.Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = [
        'screen_size', 'resolution', 'panel_type', 'hdmi_ports', 'usb_ports',
        'refresh_rate', 'operating_system', 'energy_rating', 'speaker_type',
        'connectivity', 'power_source', 'weight', 'capacity'
    ]
    search_fields = ['resolution', 'panel_type', 'operating_system', 'speaker_type', 'connectivity']
    list_filter = ['panel_type', 'operating_system', 'speaker_type', 'power_source']


admin.site.register(Product_type, ProductTypeAdmin)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'caption')
    search_fields = ('product__name', 'caption')