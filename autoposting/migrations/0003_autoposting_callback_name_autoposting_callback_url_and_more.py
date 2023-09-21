# Generated by Django 4.2.4 on 2023-08-30 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoposting', '0002_autoposting_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoposting',
            name='callback_name',
            field=models.CharField(blank=True, help_text='Не забудьте добавить ссылку в форме ниже!', max_length=25, null=True, verbose_name='Текст на кнопке'),
        ),
        migrations.AddField(
            model_name='autoposting',
            name='callback_url',
            field=models.URLField(blank=True, help_text="Это поле нужно заполнять вместе с полем 'Текст на кнопке'", null=True, verbose_name='Ссылка в кнопке'),
        ),
        migrations.AlterField(
            model_name='autoposting',
            name='accept',
            field=models.BooleanField(default=False, help_text='Это поле заполняется автоматически после подтверждения', verbose_name='Подтверждено?'),
        ),
    ]