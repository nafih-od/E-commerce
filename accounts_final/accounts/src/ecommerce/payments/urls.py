from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('payment/', views.payment_page, name='payment_page'),
    path('payment/success/', views.payment_success, name='payment_success'),
]