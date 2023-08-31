from aiogram import types, Bot
from asgiref.sync import async_to_sync
from autoposting.models import Autoposting
from decouple import config

from django.db.models.signals import post_save
from django.dispatch import receiver


def yesno(post_id) -> types.InlineKeyboardMarkup:
    yes_button, no_button = "Подтверждаю", "Не подтверждаю"
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(f"👍 {yes_button}", callback_data=f"autoposting_yes_{post_id}"),
         types.InlineKeyboardButton(f"👎 {no_button}", callback_data=f"autoposting_no_{post_id}")]
    ])
    return kb


def kb_autoposting(text, url):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text, url=url)]
    ])
    return kb


@receiver(post_save, sender=Autoposting)
def send_post_to_group(sender, instance, **kwargs):
    async def send_post():
        bot = Bot(config("BOT_TOKEN"), parse_mode=types.ParseMode.HTML)
        session = await bot.get_session()
        group_id = config("GROUP_ID")
        if instance.image:
            if instance.callback_name:
                await bot.send_photo(
                    chat_id=group_id,
                    photo=open(f'{instance.image}', 'rb'),
                    caption=instance.text,
                    reply_markup=kb_autoposting(instance.callback_name, instance.callback_url))
            else:
                await bot.send_photo(
                    chat_id=group_id,
                    photo=open(f'{instance.image}', 'rb'),
                    caption=instance.text)
        else:
            if instance.callback_name:
                await bot.send_message(
                    chat_id=group_id,
                    text=instance.text,
                    reply_markup=kb_autoposting(instance.callback_name, instance.callback_url))
            else:
                await bot.send_message(
                    chat_id=group_id,
                    text=instance.text)
        await bot.send_message(
            chat_id=group_id,
            text=f"\n\n<b>Время отправки</b>: {instance.post_time.strftime('%d.%m.%Y %H:%M')} GMT" \
                 f"\n<b>Подтвердите добавление в автопостинг:</b>",
            reply_markup=yesno(instance.id))
        await session.close()

    async_to_sync(send_post)()
