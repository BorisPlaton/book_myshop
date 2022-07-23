import csv
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from orders.models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.action(description='Export to CSV')
def export_to_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename={}.csv'.format(meta.verbose_name)
    fields = [field for field in meta.get_fields() if not (field.many_to_many or field.one_to_many)]

    writer = csv.writer(response)
    writer.writerow([field.name for field in fields])
    for obj in queryset:
        data = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime):
                value = value.strftime('%d/%m/%Y')
            data.append(value)
        writer.writerow(data)
    return response


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city', 'paid',
        'created', 'updated', 'order_detail', 'order_pdf'
    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]

    @admin.display(description='Order details')
    def order_detail(self, obj):
        return mark_safe('<a href="{}">View</a>'.format(
            reverse('orders:admin_order_detail', args=[obj.id])))

    @admin.display(description='Order pdf')
    def order_pdf(self, obj):
        return mark_safe('<a href="{}">PDF</a>'.format(
            reverse('orders:admin_order_pdf', args=[obj.id])))


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'order', 'product', 'price', 'quantity'
    ]
