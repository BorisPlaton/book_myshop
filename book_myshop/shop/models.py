from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Модель категорий товаров."""

    name = models.CharField("Category name", max_length=128, db_index=True)
    slug = models.SlugField("Category slug", max_length=128, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара."""

    category = models.ForeignKey(Category, models.CASCADE, 'products', verbose_name="Category")
    name = models.CharField("Title", max_length=128, db_index=True)
    slug = models.CharField("Slug", max_length=128, db_index=True)
    image = models.ImageField("Image", upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField("Description")
    price = models.DecimalField("Price", decimal_places=2, max_digits=10)
    available = models.BooleanField("Is available", default=True)
    created = models.DateTimeField("Created at", auto_now_add=True)
    updated = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        ordering = ['name', 'category', 'price']
        indexes = [
            models.Index(fields=['id', 'slug'], name='%(app_label)s_%(class)s_index')
        ]

    def get_absolute_url(self):
        return reverse('shop:product_view', args=[self.slug, self.pk])

    def __str__(self):
        return self.name
