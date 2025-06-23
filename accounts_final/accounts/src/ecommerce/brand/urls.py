from django.urls import path
from . import views


app_name = 'brand'

urlpatterns = [

    path('brand/', views.brand, name='brand'),
]
