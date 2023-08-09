# Generated by Django 4.2.1 on 2023-06-21 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_balance_settings'),
    ]

    operations = [
        migrations.CreateModel(
            name='NFT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='Адрес кошелька с NFT')),
                ('private_key', models.TextField(verbose_name='Приватный ключ')),
                ('tg_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.j2muser', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'NFT',
                'verbose_name_plural': 'Смарт-контракты',
            },
        ),
    ]
