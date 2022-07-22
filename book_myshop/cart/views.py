from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from cart.cart import Cart
from cart.forms import CartAddProductForm
from cart.utils import get_product_by_id


class CartDetail(TemplateView):
    """Показывает корзину пользователя."""
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request).extended_cart
        for item in cart:
            item['update_form'] = CartAddProductForm(
                initial={
                    'quantity': item['quantity'],
                    'update': True
                }
            )
        context['cart'] = cart
        return context


@require_POST
def add_product_to_cart(request, product_id):
    """Добавляет продукт в корзину."""
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.add(
            get_product_by_id(product_id),
            form.cleaned_data['quantity'],
            form.cleaned_data['update']
        )
    return redirect(reverse('cart:cart_detail'))


def remove_product_from_cart(request, product_id):
    """Удаляет полностью продукт из корзины."""
    cart = Cart(request)
    cart.remove(get_product_by_id(product_id))
    return redirect(reverse('cart:cart_detail'))
