from django.urls import path
from . import views
from .views import compare_products

urlpatterns = [

    path('products/', views.product, name="product"),
    path('compare/', compare_products, name='compare_products'),
]

app_name = "product"

