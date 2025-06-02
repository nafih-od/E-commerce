from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_email', 'is_active')
    search_fields = ('company_name', 'contact_email')