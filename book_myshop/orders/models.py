from django.db import models

from shop.models import Product


class Order(models.Model):
    """Модель заказа пользователя."""

    first_name = models.CharField("Customer's name", max_length=16)
    last_name = models.CharField("Customer's surname", max_length=16)
    email = models.EmailField("Email")
    address = models.CharField("Address", max_length=128)
    postal_code = models.CharField("Postal code", max_length=16)
    city = models.CharField("City", max_length=32)
    created = models.DateTimeField("Created at", auto_now_add=True)
    updated = models.DateTimeField("Updated at", auto_now=True)
    paid = models.BooleanField("Is order paid", default=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created']

    @property
    def order_cost(self):
        return sum([item.total_cost for item in self.order_items.all()])

    def __str__(self):
        return f"{self.pk}"


class OrderItem(models.Model):
    """Модель продукта из заказа пользователя."""

    order = models.ForeignKey(Order, verbose_name="Product order", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField("Product price", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Product quantity", default=1)

    class Meta:
        verbose_name = "Order item"
        verbose_name_plural = "Order items"
        ordering = ['-quantity']

    @property
    def total_cost(self):
        """Суммарная стоимость продукта (количество * стоимость товара)."""
        return self.price * self.quantity

    def __str__(self):
        return f"{self.pk}"
