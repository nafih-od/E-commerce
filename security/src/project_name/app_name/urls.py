from django.urls import path
from . import views

app_name = "app_name"

urlpatterns = [
    # path('', views.index, name="index"),
    path('', views.printfun, name="printfun"),
    path('ping/', views.pings, name="pings"),
    path('ssl/', views.ssl_view, name="ssl_view"),
    path('http/', views.http_view, name="http_view"),
    path('ssllabs/', views.ssllabs_view, name="ssllabs_view"),
    path('cms/', views.cms_view, name="cms_view"),
    path('ns/', views.ns_view, name="ns_view"),
    path('dt/', views.detect_view, name="detect_view"),
    path('cvt/', views.cvm_view, name="cvm_view"),

]
