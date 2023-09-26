from django.core.exceptions import ValidationError
from django.db import models
from app.models import J2MUser


class Promo(models.Model):
    tg_id = models.OneToOneField(J2MUser, verbose_name="Пользователь ID", on_delete=models.CASCADE)
    structure = models.FloatField(verbose_name="Объем структуры, USDT", null=False, default=0.0)
    percentage = models.FloatField(verbose_name="Процент депозита от объема структуры", null=False, default=10.0)
    status = models.BooleanField(verbose_name="Подтверждение включения программы", default=False)
    date_start = models.DateField(verbose_name="Дата старта программы", blank=True, null=True,
                                  help_text="После внесения даты редактировать ее будет невозможно!")
    date_end = models.DateField(verbose_name="Дата отключения программы", blank=True, null=True)
    deposit = models.FloatField(verbose_name="Активный депозит", default=0.0)
    balance = models.FloatField(verbose_name="Баланс (сумма доступная к выводу)", default=0.0)
    profit = models.FloatField(verbose_name="Доход за прошедшую неделю", default=0.0)

    def __str__(self):
        return f"Пользователь: {self.tg_id}"

    def clean(self):
        if self.status and not self.date_start:
            raise ValidationError("Нельзя подключать программу без даты старта!")
        if self.date_start and not self.status:
            raise ValidationError("Нельзя назначить дату старта без подтверждения начала!")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '[Промо] Карточка пользователя'
        verbose_name_plural = '[Промо] Пользователи'
