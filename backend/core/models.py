from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    
    # Additional Fields for Meal Planner
    dietary_preferences = models.JSONField(
        default=list,
        help_text="List of dietary preferences (e.g., ['vegetarian', 'gluten-free'])"
    )
    saved_recipes = models.JSONField(
        default=list,
        help_text="List of recipe IDs saved by the user"
    )
    fridge_inventory = models.JSONField(
        default=list,
        help_text="List of ingredients in the user's fridge (e.g., ['chicken', 'tomatoes'])"
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"

# Signal to create Account when a User is created
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

# Signal to save Account when User is saved
@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()

class Ingredient(models.Model):
    CATEGORY = [
        ('VEG', 'Vegetable'),
        ('FRUIT', 'Fruit'),
        ('LEGUME', 'Legumes & Beans'),
        ('MUSH', 'Mushroom'),
        ('GRAIN', 'Grains & Cereals'),
        ('BAKED', 'Baked Goods'),
        ('PORK', 'Pork'),
        ('CHICKEN', 'Chicken'),
        ('BEEF', 'Beef'),
        ('SEAFOOD', 'Seafood'),
        ('EGG', 'Eggs'),
        ('MEAT', 'Other Meat'),
        ('DAIRY', 'Dairy'),
        ('H&S', 'Herbs & Spices'),
        ('COND', 'Condiments & Sauces'),
        ('BEV', 'Beverages'),
        ('ALCO', 'Alcohol'),
        ('OTHER', 'Other'),
    ]

    UNITS = [
        # Weight
        ('g', 'Gram'),
        ('kg', 'Kilogram'),
        ('oz', 'Ounce'),
        ('lb', 'Pound'),

        # Volume
        ('ml', 'Milliliter'),
        ('l', 'Liter'),
        ('tsp', 'Teaspoon'),
        ('tbsp', 'Tablespoon'),
        ('cup', 'Cup'),

        # Count
        ('pc', 'Piece'),
        ('bunch', 'Bunch'),
        ('slice', 'Slice'),
        ('pack', 'Pack'),
        ('bottle', 'Bottle'),
        ('can', 'Can'),
    ]

    name = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY)
    expiration_date = models.DateField()
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, choices=UNITS)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
