from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings


def send_order_email(owner_email, product_obj, customer_obj):
    subject = "New Order Arriving"
    data = {
        "customer_email":customer_obj.user,
        "customer_phone": customer_obj.phone,
        "customer_address": customer_obj.address,
        "car": product_obj.company_name +" "+ product_obj.model_name,
        "car_number":product_obj.car_number,
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

def confirmation_mail(customer_email, product_obj):
    subject = "You Car is booked"
    data = {
        "car_type":product_obj.car_type,
        "car_owner_name":product_obj.owner_name,
        "car_company_name":product_obj.company_name,
        "car_model":product_obj.model_name,
        "car_per_day_rent":product_obj.per_day_rent
    }
    message = get_template("confirmation_mail.html").render(data)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[customer_email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    mail.send()
    return True

def decline_order_mail(customer_email, product_obj):
    subject = "Your Order Is Decline By Owner"
    data = {
        "car_type":product_obj.car_type,
        "car_owner_name":product_obj.owner_name,
        "car_company_name":product_obj.company_name,
        "car_model":product_obj.model_name,
        "car_per_day_rent":product_obj.per_day_rent
    }
    message = get_template("decline_order.html").render(data)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[customer_email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    mail.send()
    return True