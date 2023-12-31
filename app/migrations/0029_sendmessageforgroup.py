# Generated by Django 4.2.1 on 2023-06-30 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_j2muser_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendMessageForGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(choices=[('DAO', 'Владельцы NFT'), ('DU', 'Коллективный аккаунт'), ('CA', 'Личный аккаунт'), ('ALL', 'Все пользователи')], max_length=3, verbose_name='Выберите группу пользователей')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Рассылка сообщений',
            },
        ),
    ]
