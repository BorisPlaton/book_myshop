from .cart import Cart


def cart(request):
    """Возвращает объект корзины пользователя."""
    return {'cart': Cart(request)}
