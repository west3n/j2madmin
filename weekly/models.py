from django.db import models


class WeeklyBalance(models.Model):
    date = models.DateField(verbose_name="Дата расчета недельной проторговки", unique=True)
    collective_profit = models.FloatField(verbose_name='Доход коллективных аккаунтов, %', null=False, default=0.0)
    stabpool_profit = models.FloatField(verbose_name="Доход стабилизационного пула, %", null=False, default=0.0)
    is_withdrawal = models.BooleanField(verbose_name="Выводная неделя?", default=False)

    class Meta:
        verbose_name = 'Процент дохода пользователей'
        verbose_name_plural = 'Расчетный модуль'


