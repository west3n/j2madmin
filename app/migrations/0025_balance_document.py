# Generated by Django 4.2.1 on 2023-06-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='document',
            field=models.BooleanField(blank=True, null=True, verbose_name='Подтвердил ли пользователь приложение к документации'),
        ),
    ]
