# Generated by Django 4.2.4 on 2023-09-15 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoposting', '0004_autoposting_send_alter_autoposting_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoposting',
            name='post_time',
            field=models.DateTimeField(help_text='Московское время: 15.09.2023 14:05', verbose_name='Время поста'),
        ),
    ]
