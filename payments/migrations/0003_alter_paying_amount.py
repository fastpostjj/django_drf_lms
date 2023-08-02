# Generated by Django 4.2.3 on 2023-08-02 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_paying_id_intent_paying_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paying',
            name='amount',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='суммы оплаты, руб.'),
        ),
    ]
