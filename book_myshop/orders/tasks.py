from django.core.mail import send_mail

from config.celery import app
from orders.models import Order


@app.task
def order_created(order_id):
    order = Order.objects.get(pk=order_id)
    subject = "Order №{}".format(order_id)
    message = "Dear {},\n\nYou have successfully placed an order.\
                Your order id is {}.".format(order.first_name, order.id)
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent
