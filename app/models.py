from django.db import models
from django.db.models import UniqueConstraint


class Language(models.TextChoices):
    RU = 'RU', 'Русский'
    EN = 'EN', 'English'


class J2MUser(models.Model):
    tg_id = models.BigIntegerField(verbose_name='Telegram Id', primary_key=True)
    tg_username = models.CharField(verbose_name='Telegram Username', blank=True, null=True, max_length=255)
    tg_name = models.CharField(verbose_name='Полное имя', blank=True, null=True, max_length=255)
    status = models.CharField(verbose_name='Статус', blank=True, null=True, max_length=255)
    language = models.CharField(verbose_name='Язык', choices=Language.choices, null=False, max_length=2)
    alias = models.TextField(verbose_name="Почта Binance", blank=True, null=True)
    wallet = models.TextField(verbose_name="Кошелек для вывода", blank=True, null=True)
    email = models.EmailField(verbose_name="Личная почта", blank=True, null=True)

    def __str__(self):
        return f"{self.tg_username} - ID: {self.tg_id}"

    class Meta:
        verbose_name = 'Пользователь J2M'
        verbose_name_plural = 'Пользователи J2M'


class Balance(models.Model):
    tg_id = models.ForeignKey(J2MUser, verbose_name="Пользователь ID", on_delete=models.CASCADE)
    balance = models.FloatField(verbose_name="Баланс", null=False, default=0)
    deposit = models.FloatField(verbose_name="Активный депозит", null=False, default=0)
    withdrawal = models.FloatField(verbose_name="Зарезервированная сумма для вывода", blank=True, null=True)
    referral_balance = models.FloatField(verbose_name="Реферальный баланс", blank=True, null=True)
    hold = models.IntegerField(verbose_name="Выбранное количество дней холда (для 1000ников)", blank=True, null=True)
    settings = models.IntegerField(verbose_name="Настройки перевода с баланса на активный депозит (%)", blank=True, null=True)
    weekly_profit = models.FloatField(verbose_name="Доход за торговую неделю", blank=True, null=True)

    def __str__(self):
        return f"Пользователь: {self.tg_id}"

    class Meta:
        verbose_name = 'Баланс пользователя'
        verbose_name_plural = 'КОЛЛЕКТИВНЫЙ АККАУНТ - Балансы пользователей'


class BalanceStatus(models.TextChoices):
    IN = 'IN', 'Пополнение'
    OUT = 'OUT', 'Вывод'


class BalanceHistory(models.Model):
    tg_id = models.ForeignKey(J2MUser, verbose_name="Пользователь ID", on_delete=models.CASCADE)
    transaction = models.CharField(verbose_name="Статус транзакции", choices=BalanceStatus.choices, null=False,
                                   max_length=3)
    date = models.DateTimeField(verbose_name="Дата", null=False)
    amount = models.BigIntegerField(verbose_name="Сумма", null=False)
    description = models.TextField(verbose_name="Хэш транзакции", blank=True, null=True)
    status = models.BooleanField(verbose_name="Подтверждение транзакции", default=False)

    def __str__(self):
        return f"Пользователь: {self.tg_id}"

    class Meta:
        verbose_name = 'История баланса'
        verbose_name_plural = 'Истории пополнения и вывода'


class Referral(models.Model):
    tg_id = models.ForeignKey(J2MUser, verbose_name="Пользователь ID", on_delete=models.CASCADE,
                              related_name='referrals')
    line_1 = models.BigIntegerField(verbose_name="Линия 1", blank=True, null=True)
    line_2 = models.BigIntegerField(verbose_name="Линия 2", blank=True, null=True)
    line_3 = models.BigIntegerField(verbose_name="Линия 3", blank=True, null=True)

    class Meta:
        verbose_name = 'Реферальная программа'
        verbose_name_plural = 'Реферальная программа'
        constraints = [
            UniqueConstraint(fields=['tg_id', 'line_1'], name='unique_tg_id_line_1'),
            UniqueConstraint(fields=['tg_id', 'line_2'], name='unique_tg_id_line_2'),
            UniqueConstraint(fields=['tg_id', 'line_3'], name='unique_tg_id_line_3'),
        ]

    def __str__(self):
        return f"Пользователь: {self.tg_id}"


class Documents(models.Model):
    tg_id = models.ForeignKey(J2MUser, verbose_name="Пользователь", on_delete=models.CASCADE, unique=True)
    documents_approve = models.BooleanField(verbose_name="KYC верификация", default=False)
    approve_contract = models.BooleanField(verbose_name="Пользовательский контракт заполнен верно?", default=False)
    it_product = models.BooleanField(verbose_name="Подтвердил ли пользователь Приложение No 1 к Условиям применения IT продукта", blank=True,
                                   null=True)

    def __str__(self):
        return f"Пользователь: {self.tg_id}"

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Документы пользователей'


class Binance(models.Model):
    tg_id = models.OneToOneField(J2MUser, verbose_name="Пользователь", on_delete=models.CASCADE, unique=True)
    api_key = models.TextField(verbose_name="API Key", null=False)
    secret_key = models.TextField(verbose_name="API Secret key", null=False)
    balance_binance = models.FloatField(verbose_name="Баланс на Binance", blank=True, null=True)
    balance_j2m = models.FloatField(verbose_name="Баланс J2M", blank=True, null=True)
    deposit = models.FloatField(verbose_name="Активный депозит", blank=True, null=True)

    def __str__(self):
        return f"Пользователь: {self.tg_id}"

    class Meta:
        verbose_name = 'Binance API'
        verbose_name_plural = 'ЛИЧНЫЙ АККАУНТ - Балансы пользователей (Binance)'


class Thedex(models.Model):
    tg_id = models.ForeignKey(J2MUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    amount = models.BigIntegerField(verbose_name="Сумма пополнения", null=False)
    invoiceId = models.TextField(verbose_name="Уникальный номер транзакции", null=False, unique=True)
    date = models.DateTimeField(verbose_name="Время начала транзакции", null=False)
    status = models.TextField(verbose_name="Статус транзакции", blank=True, null=True)

    def __str__(self):
        return f"Пользователь: {self.tg_id}"

    class Meta:
        verbose_name = 'Thedex API'
        verbose_name_plural = 'Транзакции Thedex'


class Output(models.Model):
    tg_id = models.ForeignKey(J2MUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    amount = models.BigIntegerField(verbose_name="Сумма к выводу", null=False)
    date = models.DateTimeField(verbose_name="Дата создания заявки", null=False)
    wallet = models.TextField(verbose_name="Кошелек для вывода TRC-20", null=False)
    approve = models.BooleanField(verbose_name="Подтверждаете отправку средств на указанный кошелек?", default=False)
    hash = models.TextField(verbose_name="Хэш транзакции", blank=True, null=True)

    def __str__(self):
        return f"{self.tg_id} - Отправлено: {self.approve}"

    class Meta:
        verbose_name = 'Заявка на вывод'
        verbose_name_plural = 'Заявки на вывод средств'


class NFT(models.Model):
    tg_id = models.OneToOneField(J2MUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    invoiceId = models.TextField(verbose_name="Уникальный номер транзакции", blank=True, null=True)
    date = models.DateTimeField(verbose_name="Время начала транзакции", blank=True, null=True)
    status = models.TextField(verbose_name="Статус транзакции", blank=True, null=True)
    address = models.TextField(verbose_name="Адрес кошелька с NFT", blank=True, null=True)
    private_key = models.TextField(verbose_name="Приватный ключ", blank=True, null=True)

    def __str__(self):
        return f"Пользователь: {self.tg_id}"

    class Meta:
        verbose_name = 'NFT'
        verbose_name_plural = 'Смарт-контракты'


class Form(models.Model):
    tg_id = models.OneToOneField(J2MUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    name = models.TextField(verbose_name="ФИО", null=False)
    social = models.TextField(verbose_name="Ссылка на социальную сеть", null=False)

    def __str__(self):
        return f"Пользователь: {self.tg_id}"

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты пользователя'


class SendMessage(models.Model):
    tg_id = models.ForeignKey(J2MUser, verbose_name="Сообщение для", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст сообщения", null=False)

    def __str__(self):
        return f"Сообщение для: {self.tg_id}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Отправить сообщение пользователю'


class MessageChoice(models.TextChoices):
    DAO = "DAO", "Владельцы NFT"
    DU = "DU", "Коллективный аккаунт"
    CA = "CA", "Личный аккаунт"
    ALL = "ALL", "Все пользователи"
    EMP = "EMP", "Без смарт-контракта"


class SendMessageForGroup(models.Model):
    group = models.CharField(verbose_name="Выберите группу пользователей", choices=MessageChoice.choices, max_length=3,
                             null=False)
    text = models.TextField(verbose_name="Текст сообщения", null=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Рассылка сообщений'


class BalanceJ2M(models.Model):
    date_monday = models.DateField(verbose_name="Понедельник (Дата)", blank=True, null=True)
    balance_monday_usdt = models.BigIntegerField(verbose_name="Баланс на понедельник (USDT)", blank=True, null=True)
    balance_monday_busd = models.BigIntegerField(verbose_name="Баланс на понедельник (BUSD)", blank=True, null=True)
    date_sunday = models.DateField(verbose_name="Воскресенье (Дата)", blank=True, null=True)
    balance_sunday_usdt = models.BigIntegerField(verbose_name="Баланс на воскресенье (USDT)", blank=True, null=True)
    balance_sunday_busd = models.BigIntegerField(verbose_name="Баланс на воскресенье (BUSD)", blank=True, null=True)
    profit = models.FloatField(verbose_name="Доход % - BUSD + USDT ", blank=True, null=True)

    class Meta:
        verbose_name = 'Коллективный счет'
        verbose_name_plural = 'Расчет баланса за недельный пул'


class EveryDayBalance(models.Model):
    date = models.DateField(verbose_name="Дата", null=False)
    balance_usdt = models.BigIntegerField(verbose_name="Баланс (USDT)", blank=True, null=True)
    balance_busd = models.BigIntegerField(verbose_name="Баланс (BUSD)", blank=True, null=True)
    total = models.BigIntegerField(verbose_name="Общий баланс (без учета коэфициентов)", blank=True, null=True)


    class Meta:
        verbose_name = 'Коллективный счет'
        verbose_name_plural = 'Баланс J2M (Ежедневный)'


class APIKeys(models.Model):
    api_key = models.TextField(verbose_name="API Key", null=False)
    secret_key = models.TextField(verbose_name="Secret Key", null=False)
    description = models.TextField(verbose_name="Описание кошелька", blank=True, null=True)

    class Meta:
        verbose_name = 'Binance J2M'
        verbose_name_plural = 'Binance API J2M'



