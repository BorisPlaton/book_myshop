from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    """
    Класс для работы с корзиной товаров пользователя. Реализуется
    через сессию пользователя.
    """

    def add(self, product: Product, quantity, update=False):
        """Добавляет товар в корзину."""
        product_pk = str(product.pk)
        cart_product = self.cart.get(product_pk)

        if not cart_product:
            cart_product = self.cart[product_pk] = {
                'quantity': 0,
                'price': str(product.price),
            }

        if update:
            cart_product['quantity'] = quantity
        else:
            cart_product['quantity'] += quantity

        self.save()

    def save(self):
        """Помечает, что данные сессии изменены и их нужно сохранить."""
        self.session.modified = True

    def remove(self, product):
        """Удаляет товар из корзины."""
        try:
            del self.cart[str(product.pk)]
            self.save()
        except KeyError:
            pass

    def clear(self):
        """Очищает полностью корзину"""
        self.cart = {}
        self.save()

    @property
    def total_price(self):
        """Возвращает общую стоимость корзины."""
        return sum([Decimal(item['price']) * item['quantity'] for item in self.cart.values()])

    def __init__(self, request):
        """
        Проверяем на существование корзины пользователя, если её
        нет, то создаем заново.
        """
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID)
        if not self.cart:
            self.session[settings.CART_SESSION_ID] = self.cart = {}

    def __iter__(self):
        """
        Возвращает объект итерации, который содержит товары из
        корзины.
        """
        products = Product.objects.filter(pk__in=map(int, self.cart.keys()))

        for pk, item in self.cart.items():
            item.update({
                'total_price': Decimal(item['price']) * item['quantity'],
                'product': products.get(pk=pk)
            })
            yield item

    def __len__(self):
        """Возвращает общее количество продуктов в корзине."""
        return sum([item['quantity'] for item in self.cart.values()])
