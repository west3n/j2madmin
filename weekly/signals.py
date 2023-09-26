import asyncio

from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from weekly import models, functions
from google_sheets import old_data


@receiver(post_save, sender=models.WeeklyBalance)
def weekly_signal(sender, instance, **kwargs):
    async def get_weekly():
        await functions.count_users_profit_collective(instance.collective_profit)
        await functions.count_users_profit_stabpool(instance.stabpool_profit)
        await asyncio.sleep(60)
        await functions.send_message_with_profit_collective(instance.collective_profit)
        await asyncio.sleep(60)
        await functions.weekly_deposit_update()
        if instance.is_withdrawal:
            await functions.transfer_deposit_to_balance()
        else:
            for x in ['balance', 'stabpool']:
                await functions.balance_to_deposit_autoreinvest(x)
        await asyncio.sleep(60)
        await old_data.j2musers_sheets()
        await asyncio.sleep(30)
        await old_data.balance_sheets()
        await asyncio.sleep(30)
        await old_data.stabpool_sheets()

    async_to_sync(get_weekly)()
