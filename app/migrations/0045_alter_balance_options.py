# Generated by Django 4.2.1 on 2023-07-13 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_alter_balancehistory_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='balance',
            options={'verbose_name': 'Баланс пользователя', 'verbose_name_plural': 'КОЛЛЕКТИВНЫЙ АККАУНТ - Балансы пользователей'},
        ),
    ]
