import datetime

import aiogram.utils.exceptions
import psycopg2
from aiogram.types import ParseMode
from asgiref.sync import async_to_sync

from django.db.models.signals import post_save, post_delete
from aiogram import types, Bot, Dispatcher
from decouple import config
from django.dispatch import receiver
from app.models import Documents, Output, SendMessage, Binance, SendMessageForGroup
from google_sheets.old_data import sheets_connection


def connect():
    try:
        db = psycopg2.connect(
            host=config("DB_HOST"),
            database=config("DB_NAME"),
            user=config("DB_USER"),
            password=config("DB_PASSWORD")
        )
        cur = db.cursor()
        return db, cur
    except:
        db = psycopg2.connect(
            host=config("DB_HOST"),
            database=config("DB_NAME"),
            user=config("DB_USER"),
            password=config("DB_PASSWORD")
        )
        cur = db.cursor()
        return db, cur


async def get_language(tg_id):
    db, cur = connect()
    try:
        cur.execute("SELECT language FROM app_j2muser WHERE tg_id=%s", (tg_id,))
        result = cur.fetchone()
        return result[0]
    finally:
        db.close()
        cur.close()


async def insert_balance_history(tg_id, amount, hash):
    db, cur = connect()
    try:
        now = datetime.datetime.now()
        cur.execute("INSERT INTO app_balancehistory (tg_id_id, transaction, date, amount, status, description) "
                    "VALUES (%s, %s, %s, %s, %s, %s)", (tg_id, 'OUT', now, amount, True, hash))
        db.commit()
    finally:
        cur.close()
        db.close()


def keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Ok', callback_data='15000')]
    ])
    return kb


def keyboard_2(lang) -> types.InlineKeyboardMarkup:
    text = "Главное меню"
    if lang == "EN":
        text = "Main Menu"
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(f'{text}', callback_data="main_menu")]
    ])
    return kb


async def get_tg_id_nft():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id_id FROM app_nft WHERE status='Successful'")
        result = cur.fetchall()
        return result
    finally:
        cur.close()
        db.close()


async def get_tg_id_all():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id FROM app_j2muser")
        result = cur.fetchall()
        return result
    finally:
        cur.close()
        db.close()


async def get_tg_id_du():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id FROM app_j2muser WHERE status='500' OR status='1000'")
        result = cur.fetchall()
        return result
    finally:
        cur.close()
        db.close()


async def get_tg_id_ca():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id FROM app_j2muser WHERE status='15000'")
        result = cur.fetchall()
        return result
    finally:
        cur.close()
        db.close()


async def get_tg_id_loh():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id_id FROM app_nft WHERE status is NULL")
        result = cur.fetchall()
        return result
    finally:
        cur.close()
        db.close()


@receiver(post_save, sender=Documents)
def send_answer(sender, instance, **kwargs):
    async def send_message():
        bot = Bot(config("BOT_TOKEN"))
        session = await bot.get_session()
        tg_id = instance.tg_id_id
        language = get_language(tg_id)
        text = "Администратор проверил документ и передал его в Binance. " \
               "В течении 4 рабочих дней Binance оповестит Вас по электронной почте указанной в договоре " \
               "о том, что Вам доступен функционал управляемых субсчетов." \
               "\n\nПосле получения этого уведомления от Binance, Вам нужно совершить следующие шаги:\n" \
               "\n1. Зайдите с компьютера или ноутбука в свой профиль Binance (иконка Вашего профиля вверху справа)." \
               "\n2.В открывшемся меню, снизу появился раздел “Субаккаунты”." \
               "\n3. Слева в меню раздела нажмите “Управляемый субаккаунт” Будьте внимательны, не спутав его с " \
               "разделом “Управление аккаунтом”" \
               "Откроется страница настройки управляемых субаккаунтов. " \
               "В правом верхнем углу нажмите на кнопку “Создать управляемый субаккаунт”." \
               "Появится окно создания субаккаунта." \
               "Нужно ввести название счета. Название счёта должно быть написано латинскими буквами и содержать ваши " \
               "Имя и Фамилию. Данная информация нужна, чтобы наши технические специалисты могли идентифицировать Вас" \
               " в клиентской базе." \
               "Указываете наш UID2 и наш email, которые Вам отправил наш администратор." \
               "Система запросит подтверждение операции. " \
               "После подтверждения система присвоит субсчету виртуальный адрес электронной почты (alias), " \
               "который будет начинаться с указанного Вами ранее nickname." \
               "\n\nПодробная инструкция по " \
               "<a href='https://teletype.in/@lmarket/podkluchenie-subakkaunta-sonera-saina-instrukciya'>ccылке</a> "
        if language == "EN":
            text = "The administrator has reviewed your document and forwarded it to Binance. " \
                   "Within 4 business days, Binance will notify you via the email provided in the contract " \
                   "that you have access to managed subaccounts functionality." \
                   "\n\nAfter receiving this notification from Binance, you need to take the following steps:" \
                   "\n\n1. Log in to your Binance profile from a computer or laptop (profile icon in the top right " \
                   "corner)." \
                   "\n2. In the menu that appears at the bottom, select 'Subaccounts'." \
                   "\n3. On the left side of the subaccounts section, click on 'Managed Subaccount'. Be careful not " \
                   "to confuse it " \
                   "with the 'Account Management' section." \
                   "\n\nThe managed subaccounts settings page will open. In the top right corner, click on 'Create " \
                   "Managed Subaccount'." \
                   "A subaccount creation window will appear." \
                   "Enter the account name. The account name should be written in Latin letters and include your " \
                   "First Name and Last Name. This information is needed for our technical specialists to identify " \
                   "you in the customer database." \
                   "Specify our UID2 and our email, which our administrator sent to you." \
                   "The system will request confirmation of the operation. " \
                   "After confirmation, the system will assign a virtual email address (alias) to the subaccount, " \
                   "which will start with the nickname you previously provided." \
                   "\n\nDetailed instructions can be found at the following " \
                   "<a href='https://teletype.in/@lmarket/podkluchenie-subakkaunta-sonera-saina-instrukciya'>link</a>."
        await bot.send_message(chat_id=tg_id,
                               text=text,
                               reply_markup=keyboard(),
                               parse_mode=ParseMode.HTML,
                               disable_notification=True,
                               disable_web_page_preview=True)
        await session.close()

    async_to_sync(send_message)()


@receiver(post_delete, sender=Documents)
def send_answer(sender, instance, **kwargs):
    async def send_message():
        bot = Bot(config("BOT_TOKEN"))
        session = await bot.get_session()
        tg_id = instance.tg_id_id
        language = get_language(tg_id)
        text = "Администратор отклонил ваш контракт, " \
               "для подробностей напишите в <a href='https://t.me/J2M_Support'>Поддержку</a>"
        if language == "EN":
            text = "The administrator has rejected your contract. For details, " \
                   "please contact <a href='https://t.me/J2M_Support'>Support</a>."
        await bot.send_message(chat_id=tg_id,
                               text=text,
                               reply_markup=keyboard(),
                               parse_mode=ParseMode.HTML,
                               disable_notification=True,
                               disable_web_page_preview=True)
        await session.close()

    async_to_sync(send_message)()


@receiver(post_save, sender=Output)
def send_answer(sender, instance, **kwargs):
    async def send_message():
        bot = Bot(config("BOT_TOKEN"))
        session = await bot.get_session()
        tg_id = instance.tg_id_id
        language = get_language(tg_id)
        db, cur = connect()
        try:
            cur.execute("INSERT INTO app_balancehistory (tg_id_id, transaction, date, amount, description, status) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (tg_id, "OUT", datetime.datetime.now(), instance.amount, instance.hash, True,))
            db.commit()
            cur.execute("UPDATE app_balance SET withdrawal=0 WHERE tg_id_id = %s", (tg_id,))
            db.commit()
            sh = await sheets_connection()
            worksheet_name = "Сумма пополнения пула"
            worksheet = sh.worksheet(worksheet_name)
            worksheet.append_row((datetime.datetime.now().date().strftime("%Y-%m-%d"),
                                  tg_id, "Вывод", f"-{instance.amount}"))
        finally:
            db.close()
            cur.close()
        text = f"Средства ({instance.amount} USDT) успешно выведены!\n\n" \
               f"Хэш транзакции: {instance.hash}"

        if language == "EN":
            text = f"Funds ({instance.amount} USDT) have been successfully withdrawn!\n\n"
            f"Transaction hash: {instance.hash}"
        await bot.send_message(chat_id=tg_id,
                               text=text,
                               reply_markup=keyboard_2(language),
                               parse_mode=ParseMode.HTML,
                               disable_notification=True,
                               disable_web_page_preview=True)
        await session.close()

    async_to_sync(send_message)()


@receiver(post_delete, sender=Output)
def send_answer(sender, instance, **kwargs):
    async def send_message():
        bot = Bot(config("BOT_TOKEN"))
        session = await bot.get_session()
        tg_id = instance.tg_id_id
        language = get_language(tg_id)
        text = "<b>Администратор отменил вашу заявку на вывод, для подробностей напишите " \
               "в <a href='https://t.me/J2M_Support'>Поддержку</a></b>"
        if language == "EN":
            text = "<b>The administrator has canceled your withdrawal request. " \
                   "For details, please contact <a href='https://t.me/J2M_Support'>Support</a>.</b>"
        await bot.send_message(chat_id=tg_id,
                               text=text,
                               reply_markup=keyboard_2(language),
                               parse_mode=ParseMode.HTML,
                               disable_notification=True,
                               disable_web_page_preview=True)
        await session.close()

    async_to_sync(send_message)()


@receiver(post_save, sender=SendMessage)
def send_message_for_user(sender, instance, **kwargs):
    async def send_message():
        bot = Bot(config("BOT_TOKEN"))
        session = await bot.get_session()
        tg_id = instance.tg_id_id
        language = get_language(tg_id)
        text = f"<b>Администратор отправил вам сообщение:</b>\n\n" \
               f"<em>{instance.text}</em>"
        if language == "EN":
            text = "<b>Administrator send message for you:</b>\n\n" \
                   f"<em>{instance.text}</em>"
        await bot.send_message(chat_id=tg_id,
                               text=text,
                               parse_mode=ParseMode.HTML,
                               disable_notification=True,
                               disable_web_page_preview=True)
        await session.close()

    async_to_sync(send_message)()


@receiver(post_save, sender=Binance)
def send_message_for_user(sender, instance, **kwargs):
    async def send_message():
        bot = Bot(config("BOT_TOKEN"))
        session = await bot.get_session()
        tg_id = instance.tg_id_id
        language = get_language(tg_id)
        text = f"Администратор подтвердил ваши данные по API KEY, API SECRET, Alias"
        if language == "EN":
            text = f"<b>The administrator has confirmed your API KEY, API SECRET, and Alias.</b>"
        await bot.send_message(chat_id=tg_id,
                               text=text,
                               parse_mode=ParseMode.HTML,
                               disable_notification=True,
                               disable_web_page_preview=True)
        await session.close()

    async_to_sync(send_message)()


@receiver(post_save, sender=SendMessageForGroup)
def send_message_for_user(sender, instance, **kwargs):
    async def send_message():
        bot = Bot(config("BOT_TOKEN"))
        session = await bot.get_session()
        tg_ids = await get_tg_id_all()
        if instance.group == "DAO":
            tg_ids = await get_tg_id_nft()
        if instance.group == "DU":
            tg_ids = await get_tg_id_du()
        if instance.group == "CA":
            tg_ids = await get_tg_id_ca()
        if instance.group == "EMP":
            tg_ids = await get_tg_id_loh()

        for tg_id in tg_ids:
            language = get_language(tg_id[0])
            text = f"<em>Администратор отправил сообщение:</em>\n\n" \
                   f"{instance.text}"
            if language == "EN":
                text = f"<em>The administrator send message:</em>" \
                       f"{instance.text}"
            try:
                await bot.send_message(chat_id=tg_id[0],
                                       text=text,
                                       parse_mode=ParseMode.HTML,
                                       disable_notification=True,
                                       disable_web_page_preview=True)
            except aiogram.utils.exceptions.BotBlocked:
                pass
        await session.close()

    async_to_sync(send_message)()
