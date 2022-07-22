from django.urls import path

from orders.views import CreateOrder


app_name = 'orders'

urlpatterns = [
    path('create/', CreateOrder.as_view(), name='create_order'),
]
