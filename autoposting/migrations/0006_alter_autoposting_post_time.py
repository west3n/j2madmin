# Generated by Django 4.2.4 on 2023-09-15 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoposting', '0005_alter_autoposting_post_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoposting',
            name='post_time',
            field=models.DateTimeField(help_text='Московское время: 15.09.2023 14:09', verbose_name='Время поста'),
        ),
    ]
