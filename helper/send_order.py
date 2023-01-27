from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings


def send_order_email(owner_email, product_id, customer_obj):
    subject = "New Order Arriving"
    data = {
        "customer_email":customer_obj.user,
        "product_id": product_id,
        "customer_phone": customer_obj.phone,
        "customer_address": customer_obj.address,
    }
    message = get_template("order_car.html").render(data)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[owner_email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    mail.send()
    return True
