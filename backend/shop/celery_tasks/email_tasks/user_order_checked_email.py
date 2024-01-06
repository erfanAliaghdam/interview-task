from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from_email = settings.FROM_EMAIL


@shared_task(max_retries=5, retry_backoff=True)
def user_order_checked_email(
    email: str, first_name: str, last_name: str, order_id: int
):
    send_mail(
        subject="order approved",
        message=f"""
            Hey dear{first_name} {last_name},
            your order with id :{order_id}, has been checked by our team.

        """,
        from_email=from_email,
        recipient_list=[email],
        fail_silently=True,
    )
