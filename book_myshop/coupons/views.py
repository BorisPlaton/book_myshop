from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import FormView

from coupons.forms import CouponApplyForm
from coupons.models import Coupon


@method_decorator(require_POST, name='dispatch')
class CouponApply(FormView):
    form_class = CouponApplyForm
    success_url = reverse_lazy('cart:cart_detail')

    def form_valid(self, form):
        try:
            now = timezone.now()
            coupon = Coupon.objects.get(
                code=form.cleaned_data['code'],
                active=True,
                valid_from__lte=now,
                valid_to__gte=now
            )
            self.request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            self.request.session['coupon_id'] = None
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect(self.success_url)
