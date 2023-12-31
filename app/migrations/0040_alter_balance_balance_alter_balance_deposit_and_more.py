# Generated by Django 4.2.1 on 2023-07-07 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_rename_weakly_profit_balance_weekly_profit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='balance',
            field=models.FloatField(default=0, verbose_name='Баланс'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='deposit',
            field=models.FloatField(default=0, verbose_name='Активный депозит'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='referral_balance',
            field=models.FloatField(blank=True, null=True, verbose_name='Реферальный баланс'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='weekly_profit',
            field=models.FloatField(blank=True, null=True, verbose_name='Доход за торговую неделю'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='withdrawal',
            field=models.FloatField(blank=True, null=True, verbose_name='Зарезервированная сумма для вывода'),
        ),
    ]
