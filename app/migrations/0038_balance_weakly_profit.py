# Generated by Django 4.2.1 on 2023-07-06 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_rename_balance_monday_balancej2m_balance_monday_usdt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='weakly_profit',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Доход за торговую неделю'),
        ),
    ]
