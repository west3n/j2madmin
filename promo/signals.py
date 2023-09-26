import datetime

import decouple
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from promo.models import Promo
from django.dispatch import receiver
from aiogram import Bot


@receiver(post_save, sender=Promo)
def insert_date_end(sender, instance, **kwargs):
    if instance.date_start:
        date_end = instance.date_start + datetime.timedelta(days=365)
        Promo.objects.filter(tg_id_id=instance.tg_id).update(date_end=date_end)
    if instance.status and not instance.date_end:
        async def send_message():
            bot = Bot(token=decouple.config("BOT_TOKEN"))
            session = await bot.get_session()
            end_date = instance.date_start + datetime.timedelta(days=365)
            await bot.send_message(
                instance.tg_id_id, 'Ваша заявка на подключение к промо-программе одобрена!'
                                   f'\nДата начала: {instance.date_start.strftime("%d.%m.%Y")}'
                                   f'\nДата окончания: {end_date.strftime("%d.%m.%Y")}'
                                   f'\nОбъем структуры: {instance.structure} USDT'
                                   f'\nПроцент от структуры: {instance.percentage}%'
                                   f'\nПромо-депозит: {instance.deposit} USDT'
            )
            await session.close()

        async_to_sync(send_message)()
