from django.urls import path
from .views import category_list, category_detail

urlpatterns = [

    path('categories/', category_list, name='category_list'),
    path("<slug:slug>/", category_detail, name="category_detail"),

]