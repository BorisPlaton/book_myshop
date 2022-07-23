from django_redis import get_redis_connection
from redis.client import StrictRedis

from shop.models import Product


class Recommender:

    def __init__(self):
        self.con: StrictRedis = get_redis_connection('recommender')

    @staticmethod
    def get_product_key(pk):
        return 'product:{}:purchased_with'.format(pk)

    def update_products_bought_with(self, products):
        """Обновляет список товаров с которыми покупается вещь."""
        products_id = [product.id for product in products]

        for product_id in products_id:
            for product_with_id in products_id:
                if product_id == product_with_id:
                    continue
                self.con.zincrby(
                    self.get_product_key(product_id),
                    1,
                    product_with_id
                )

    def get_recommendation_for(self, products_list: list, max_results=3):
        """Возвращает рекомендации для списка товаров."""
        products_ids = [product.pk for product in products_list]
        if len(products_ids) == 1:
            suggestions_items_id = self.con.zrange(self.get_product_key(products_ids[0]), 0, -1, True)[:max_results]
        else:
            suggested_items_list_label = 'suggested_zset'
            self.con.zunionstore(
                suggested_items_list_label,
                [self.get_product_key(product_ids) for product_ids in products_ids]
            )
            self.con.zrem(
                suggested_items_list_label,
                *products_ids
            )
            suggestions_items_id = self.con.zrange(suggested_items_list_label, 0, -1, True)[:max_results]
            self.con.delete(suggested_items_list_label)
        suggestions_items = list(Product.objects.filter(pk__in=map(int, suggestions_items_id)))
        return suggestions_items

    def clear_recommendations(self):
        """Очищает все рекомендации для товаров."""
        self.con.delete([self.get_product_key(pk) for pk in Product.objects.values_list('id', flat=True)])
