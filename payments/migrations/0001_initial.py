# Generated by Django 4.2.4 on 2023-08-24 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paying',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_pay', models.DateField(auto_now=True, verbose_name='дата платежа')),
                ('amount', models.FloatField(blank=True, default=0.0, null=True, verbose_name='суммы оплаты, руб.')),
                ('payment_method', models.CharField(choices=[('cash', 'наличные'), ('transfer', 'перевод на счет'), ('card', 'оплата картой')], default='transfer', max_length=15, verbose_name='Способ оплаты')),
                ('id_intent', models.CharField(blank=True, max_length=50, null=True, verbose_name='id намерения платежа')),
                ('status', models.CharField(blank=True, max_length=200, null=True, verbose_name='статус платежа')),
            ],
            options={
                'verbose_name': 'платеж',
                'verbose_name_plural': 'платежи',
            },
        ),
    ]
