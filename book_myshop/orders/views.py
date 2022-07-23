import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order
from orders.tasks import order_created


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
        cart = Cart(self.request)
        order = self.get_form().save(commit=False)
        if cart.coupon:
            order.coupon = cart.coupon
            order.discount = cart.coupon.discount
        order.save()
        for item in cart.extended_cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=float(item['price']),
                quantity=item['quantity'],
            )
        cart.clear()
        order_created(order.id)
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderDetail(DetailView):
    model = Order
    template_name = 'orders/admin/order_detail.html'
    context_object_name = 'order'


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    html_pdf = render_to_string(
        'orders/pdf.html',
        {'order': order}
    )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename=order_{}.csv'.format(order.id)
    weasyprint.HTML(string=html_pdf).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT / 'orders/css/pdf.css'
        )]
    )
    return response
