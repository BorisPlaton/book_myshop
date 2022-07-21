from django.urls import path

from cart.views import CartDetail, remove_product_from_cart, add_product_to_cart


app_name = 'cart'

urlpatterns = [
    path('', CartDetail.as_view(), name='cart_detail'),
    path('remove/product/<int:product_id>', remove_product_from_cart, name='remove_product'),
    path('add/product/<int:product_id>', add_product_to_cart, name='add_product'),
]
