# Generated by Django 4.2.1 on 2023-06-19 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_j2muser_wallet_alter_j2muser_alias_output'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='hold',
            field=models.IntegerField(blank=True, null=True, verbose_name='Выбранное количество дней холда (для 1000ников)'),
        ),
    ]
