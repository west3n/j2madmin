# Generated by Django 4.2.4 on 2023-09-26 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoposting', '0010_alter_autoposting_post_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoposting',
            name='post_time',
            field=models.DateTimeField(help_text='Московское время: 26.09.2023 13:25', verbose_name='Время поста'),
        ),
    ]