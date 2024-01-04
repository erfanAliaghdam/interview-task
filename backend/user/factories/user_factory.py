from django.contrib.auth import get_user_model
import factory
from django.contrib.auth.models import Group


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.Faker("password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @factory.post_generation
    def assign_to_group(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        group_name = extracted
        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)
