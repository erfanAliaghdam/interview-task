from django.conf import settings
from django.contrib.auth import get_user_model

from shop.models import Product
from user.factories import UserFactory, GroupFactory
from shop.factories import ProductFactory


def generate_development_seed():
    superuser_email = "superuser@example.com"
    default_password = "DefaultPassword"
    get_user_model().objects.create_superuser(
        email=superuser_email, password=default_password
    )
    print("!!! superuser email for development environment: ", superuser_email, " !!!")
    print(
        "!!! superuser password for development environment: ", default_password, " !!!"
    )
    print("\n wait .....")
    groups_list = settings.GROUP_LIST
    for group in groups_list:
        GroupFactory.create(name=group)
    UserFactory.create_batch(10, assign_to_group="Client")

    client_user = UserFactory.create(
        assign_to_group="Client", email="client@example.com"
    )

    client_user.set_password(default_password)
    client_user.save()

    print(
        "!!! client user email for development environment: ", client_user.email, " !!!"
    )
    print(
        "!!! support user password for development environment: ",
        default_password,
        " !!!",
    )

    print(str(get_user_model().objects.all().count()), "users created. ")

    ProductFactory.create_batch(5, stock=0)
    ProductFactory.create_batch(20)
    print(str(Product.objects.all().count()), "products created. ")

