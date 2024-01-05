from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from shop.repositories import OrderRepository
from datetime import datetime, timedelta

from_email = settings.FROM_EMAIL
superuser_email = settings.SUPERUSER_EMAIL
order_repository = OrderRepository()


@shared_task(max_retries=5, retry_backoff=True)
def checked_orders():
    now = datetime.now()

    # Calculate the datetime of yesterday
    yesterday = now - timedelta(days=1)

    # Set the time to 8 PM
    yesterday_8pm = datetime(yesterday.year, yesterday.month, yesterday.day, 20, 0, 0)
    orders_count = order_repository.get_checked_order_count_by_created_at_range(
        start=yesterday_8pm,
        finish=now
    )

    send_mail(
        subject="order approved",
        message=f"""
            Dear Admin,

            Total orders processed from last night to now: [{orders_count}].
        """,
        from_email=from_email,
        recipient_list=[superuser_email],
        fail_silently=True
    )
