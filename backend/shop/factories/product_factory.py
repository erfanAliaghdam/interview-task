from shop.models import Product
import factory
import random


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    price = random.choice(range(1, 250))
    stock = random.choice(range(1, 5))
