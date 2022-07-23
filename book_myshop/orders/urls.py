from django.urls import path

from orders.views import CreateOrder, AdminOrderDetail, admin_order_pdf


app_name = 'orders'

urlpatterns = [
    path('create/', CreateOrder.as_view(), name='create_order'),
    path('details/<int:pk>/', AdminOrderDetail.as_view(), name='admin_order_detail'),
    path('pdf/<int:order_id>/', admin_order_pdf, name='admin_order_pdf'),
]
