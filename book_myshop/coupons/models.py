from django.core.validators import MaxValueValidator
from django.db import models


class Coupon(models.Model):
    """Модель купона на скидку товара."""

    code = models.CharField("Coupon unique code", max_length=50, unique=True)
    valid_from = models.DateTimeField("Valid from")
    valid_to = models.DateTimeField("Valid to")
    discount = models.PositiveIntegerField("Discount", validators=[MaxValueValidator(100)])
    active = models.BooleanField("Is active")

    def __str__(self):
        return self.code
