from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path('confirm/', views.confirm_cart, name='confirm_cart'),
    path("add/<uuid:product_id>/", views.add_to_cart, name="add"),
    path("place-order/<uuid:product_id>/", views.place_temp_order, name="place_temp_order"),
    path("review-order/<int:order_id>/", views.review_temp_order, name="review_temp_order"),
    path('remove/<int:item_id>/', views.remove_item, name='remove_item'),
    path('view/', views.cart_view, name='cart_view'),


]
