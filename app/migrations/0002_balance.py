# Generated by Django 4.2.1 on 2023-05-25 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.BigIntegerField(default=0, verbose_name='Balance')),
                ('deposit', models.BigIntegerField(default=0, verbose_name='Active deposit')),
                ('tg_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.j2muser', verbose_name='User ID')),
            ],
        ),
    ]