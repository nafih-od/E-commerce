from django.urls import path, include

from account.views import index, login_user, register_user
from category.views import product_detail
from ecommerce import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("category/", include("category.urls")),
    path('', include("account.urls", namespace="account")),
    path('', include("product.urls", namespace="product")),
    path('', include("brand.urls", namespace="brand")),
    path('', include("payments.urls", namespace="payments")),
    path('', include("vendor.urls", namespace="vendor")),
    path("cart/", include("cart.urls", namespace="cart")),
    path('product/<uuid:pk>/', product_detail, name='product_detail'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
