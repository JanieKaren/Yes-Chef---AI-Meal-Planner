import factory
from django.contrib.auth import get_user_model
from core.models import Ingredient
import random
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'defaultpass')

class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    user = factory.LazyFunction(lambda: random.choice(get_user_model().objects.all()))
    name = factory.Faker('word')
    icon_name = factory.Faker('emoji')
    category = factory.LazyFunction(lambda: random.choice([choice[0] for choice in Ingredient.CATEGORY]))
    expiration_date = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=random.randint(1, 30)))
    quantity = factory.Faker('pyint', min_value=1)
    unit = factory.LazyFunction(lambda: random.choice([choice[0] for choice in Ingredient.UNITS]))

    