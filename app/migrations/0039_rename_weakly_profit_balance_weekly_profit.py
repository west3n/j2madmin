# Generated by Django 4.2.1 on 2023-07-06 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_balance_weakly_profit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balance',
            old_name='weakly_profit',
            new_name='weekly_profit',
        ),
    ]
