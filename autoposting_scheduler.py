import datetime
import asyncio

from aiogram import types, Bot
from aiogram.types import InputFile
from database.injector import connect
from decouple import config

bot = Bot(config("BOT_TOKEN"), parse_mode=types.ParseMode.HTML)
group_id = config('GROUP_ID')


def kb_autoposting(text, url):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text, url=url)]
    ])
    return kb


async def get_autopost_data():
    db, cur = connect()
    try:
        cur.execute("SELECT * FROM autoposting_autoposting WHERE post_time <= now() AND accept = true AND send = false")
        result = cur.fetchone()
        # [0]: id, [1]: text, [2]: post_time, [3]: accept [4]: image, [5]: callback_name, [6]: callback_url, [7]: send
        if result:
            new_result = [result[x] for x in range(0, 7) if x != 3]
            return new_result
    finally:
        cur.close()
        db.close()


async def post_send_true(post_id):
    db, cur = connect()
    try:
        cur.execute("UPDATE autoposting_autoposting SET send = true WHERE id = %s", (post_id,))
        db.commit()
    finally:
        cur.close()
        db.close()


async def autoposting_task():
    print(f"Задача по автопостингу запущена в {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}")
    while True:
        data = await get_autopost_data()
        if data:
            post_id, text, post_time, image, callback_name, callback_url = data
            if not image and not callback_name:
                await bot.send_message(group_id, text)
            elif not callback_name:
                await bot.send_photo(group_id, InputFile(image), text)
            elif not image:
                await bot.send_message(group_id, text, reply_markup=kb_autoposting(callback_name, callback_url))
            else:
                await bot.send_photo(
                    group_id, InputFile(image), text, reply_markup=kb_autoposting(callback_name, callback_url))
            await post_send_true(post_id)
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(autoposting_task())
