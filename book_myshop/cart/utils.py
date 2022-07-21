from django.shortcuts import get_object_or_404

from shop.models import Product


def get_product_by_id(pk: int) -> Product:
    """
    Возвращает объект модели `shop.models.Product`, если
    не существует, возвращает 404 ошибку.
    """
    return get_object_or_404(Product, pk=pk)
