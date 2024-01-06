from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.repositories import CartRepository

cart_repository = CartRepository()


@receiver(post_save, sender=get_user_model())
def create_user_cart_on_user_creation(sender, instance, created, **kwargs):
    if created:
        cart_repository.create_get_or_create_cart_for_user_by_user_id(
            user_id=instance.id
        )
