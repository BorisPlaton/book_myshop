from django.urls import path

from coupons.views import CouponApply


app_name = 'coupons'

urlpatterns = [
    path('activate/', CouponApply.as_view(), name='activate_coupon'),
]
