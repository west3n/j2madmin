# Generated by Django 4.2.1 on 2023-06-26 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_balance_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('tg_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.j2muser', verbose_name='Сообщение для')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Отправить сообщение пользователю',
            },
        ),
    ]