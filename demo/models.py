from django.db import models
from app.models import J2MUser


class DemoUser(models.Model):
    tg_id = models.OneToOneField(J2MUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    balance_collective = models.FloatField(verbose_name="Баланс коллективный ДЕМО", null=False, default=0)
    deposit_collective = models.FloatField(verbose_name="Активный депозит коллективный ДЕМО", null=False, default=0)
    api_key = models.TextField(verbose_name="API Key ДЕМО", blank=True, null=True)
    secret_key = models.TextField(verbose_name="API Secret key ДЕМО", blank=True, null=True)
    balance_binance = models.FloatField(verbose_name="Баланс на Binance ДЕМО", blank=True, null=True)
    balance_personal = models.FloatField(verbose_name="Баланс J2M ДЕМО", blank=True, null=True)
    deposit_personal = models.FloatField(verbose_name="Активный депозит ДЕМО", blank=True, null=True)

    def __str__(self):
        return f"{self.tg_id}"

    class Meta:
        verbose_name = '[Демо] Баланс пользователя'
        verbose_name_plural = '[Демо] Балансы пользователя'


class BalanceStatus(models.TextChoices):
    IN = 'IN', 'Пополнение'
    OUT = 'OUT', 'Вывод'


class DemoBalanceHistory(models.Model):
    tg_id = models.ForeignKey(J2MUser, verbose_name="Пользователь ID", on_delete=models.CASCADE)
    transaction = models.CharField(verbose_name="Статус транзакции", choices=BalanceStatus.choices, null=False,
                                   max_length=3)
    transaction_type = models.TextField(verbose_name="Тип аккаунта", null=True, blank=True)
    date = models.DateTimeField(verbose_name="Дата", null=False)
    amount = models.BigIntegerField(verbose_name="Сумма", null=False)
    description = models.TextField(verbose_name="Хэш транзакции", blank=True, null=True)
    status = models.BooleanField(verbose_name="Подтверждение транзакции", default=False)

    def __str__(self):
        return f"{self.tg_id}"

    class Meta:
        verbose_name = '[Демо] История баланса'
        verbose_name_plural = '[Демо] История пополнения и вывода'


class DemoStabPool(models.Model):
    tg_id = models.ForeignKey(J2MUser, verbose_name="Пользователь ID", on_delete=models.CASCADE)
    balance = models.FloatField(verbose_name="Баланс", null=False, default=0)
    deposit = models.FloatField(verbose_name="Активный депозит", null=False, default=0)
    withdrawal = models.FloatField(verbose_name="Зарезервированная сумма для вывода", blank=True, null=True)
    hold = models.IntegerField(verbose_name="Количество дней холда", blank=True, null=True)
    weekly_profit = models.FloatField(verbose_name="Доход за торговую неделю", blank=True, null=True)

    def __str__(self):
        return f"Пользователь: {self.tg_id}"

    class Meta:
        verbose_name = '[Демо] Баланс пользователя'
        verbose_name_plural = '[Демо] СТАБИЛИЗАЦИОННЫЙ ПУЛ - Балансы пользователей'
