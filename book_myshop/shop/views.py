from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from shop.models import Product, Category


class ProductView(DetailView):
    """Показывает страницу одного товара."""
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'


class ProductList(ListView):
    """Показывает список всех доступных товаров."""

    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = self.model.objects.filter(
            available=True
        ).all()
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductListByCategory(ProductList):
    """Показывает список товаров по категории."""

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        products = super().get_queryset().filter(
            category=self.category
        )
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['products_category'] = self.category
        return context
