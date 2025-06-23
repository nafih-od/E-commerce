from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [

    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('index/', views.index, name='index'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile_detail, name='profile_detail'),
]

