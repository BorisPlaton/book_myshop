from django.urls import path

from shop.views import ProductView, ProductList, ProductListByCategory


app_name = 'shop'

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('<slug:category_slug>/', ProductListByCategory.as_view(), name='product_list_by_category'),
    path('<slug:slug>/<int:pk>/', ProductView.as_view(), name='product_view'),
]
