# Generated by Django 4.2.1 on 2023-05-28 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_referal_referral'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='balance',
            options={'verbose_name': 'Баланс пользователя', 'verbose_name_plural': 'Балансы пользователей'},
        ),
        migrations.AlterModelOptions(
            name='balancehistory',
            options={'verbose_name': 'История баланса', 'verbose_name_plural': 'Истории пополнения и вывода'},
        ),
        migrations.AlterModelOptions(
            name='j2muser',
            options={'verbose_name': 'Пользователь J2M', 'verbose_name_plural': 'Пользователи J2M'},
        ),
        migrations.AlterModelOptions(
            name='referral',
            options={'verbose_name': 'Реферальная программа', 'verbose_name_plural': 'Реферальная программа'},
        ),
        migrations.AlterField(
            model_name='balance',
            name='balance',
            field=models.BigIntegerField(default=0, verbose_name='Баланс'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='deposit',
            field=models.BigIntegerField(default=0, verbose_name='Активный депозит'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='tg_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.j2muser', verbose_name='Пользователь ID'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='withdrawal',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Зарезервированная сумма для вывода'),
        ),
        migrations.AlterField(
            model_name='balancehistory',
            name='amount',
            field=models.BigIntegerField(verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='balancehistory',
            name='date',
            field=models.DateTimeField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='balancehistory',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='balancehistory',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Подтверждение транзакции'),
        ),
        migrations.AlterField(
            model_name='balancehistory',
            name='tg_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.j2muser', verbose_name='Пользователь ID'),
        ),
        migrations.AlterField(
            model_name='balancehistory',
            name='transaction',
            field=models.CharField(choices=[('IN', 'Пополнение'), ('OUT', 'Вывод')], max_length=3, verbose_name='Статус транзакции'),
        ),
        migrations.AlterField(
            model_name='referral',
            name='line_1',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Линия 1'),
        ),
        migrations.AlterField(
            model_name='referral',
            name='line_2',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Линия 2'),
        ),
        migrations.AlterField(
            model_name='referral',
            name='line_3',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Линия 3'),
        ),
        migrations.AlterField(
            model_name='referral',
            name='tg_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrals', to='app.j2muser', verbose_name='Пользователь ID'),
        ),
    ]