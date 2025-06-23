from django.urls import path
from .views import vendor_dashboard, add_product, become_vendor

app_name = "vendor"

urlpatterns = [
    path('vendor_dashboard/', vendor_dashboard, name='vendor_dashboard'),
    path('add-product/', add_product, name='add_product'),
    path('become-vendor/', become_vendor, name='become_vendor'),
]
