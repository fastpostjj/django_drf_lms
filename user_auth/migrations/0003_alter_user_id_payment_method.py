# Generated by Django 4.2.3 on 2023-08-01 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_user_id_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id_payment_method',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='id метода платежа'),
        ),
    ]
