# Generated by Django 5.2 on 2025-06-05 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_account_allergies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='fridge_inventory',
        ),
    ]
