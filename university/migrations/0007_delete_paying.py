# Generated by Django 4.2.3 on 2023-07-29 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0006_remove_subscription_subscribed'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Paying',
        ),
    ]
