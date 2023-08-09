# Generated by Django 4.2.1 on 2023-07-05 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_alter_sendmessageforgroup_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceJ2M',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('balance', models.BigIntegerField(verbose_name='Баланс (USDT)')),
            ],
            options={
                'verbose_name': 'Коллективный счет',
                'verbose_name_plural': 'Баланс J2M',
            },
        ),
    ]