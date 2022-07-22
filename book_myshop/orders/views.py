from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem


class CreateOrder(FormView):
    """Страница создания заказа."""

    template_name = 'orders/create_order.html'
    form_class = OrderCreateForm

    success_url = reverse_lazy('shop:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

    def form_valid(self, form):
        order = self.get_form().save()
        cart = Cart(self.request)
        for item in cart.extended_cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=float(item['price']),
                quantity=item['quantity'],
            )
        cart.clear()
        return super().form_valid(form)
