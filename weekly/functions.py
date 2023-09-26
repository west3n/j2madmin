import psycopg2

from aiogram import types, Bot
from aiogram.utils.exceptions import BotBlocked
from decouple import config
from datetime import datetime


def connect():
    try:
        db = psycopg2.connect(
            host=config("DB_HOST"),
            database=config("DB_NAME"),
            user=config("DB_USER"),
            password=config("DB_PASS")
        )
        cur = db.cursor()
        return db, cur
    except psycopg2.Error:
        db = psycopg2.connect(
            host=config("DB_HOST"),
            database=config("DB_NAME"),
            user=config("DB_USER"),
            password=config("DB_PASS")
        )
        cur = db.cursor()
        return db, cur


async def get_all_tg_id():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id FROM app_j2muser")
        return [tg_id[0] for tg_id in cur.fetchall()]
    finally:
        db.close()
        cur.close()


async def get_my_balance(tg_id, table):
    db, cur = connect()
    try:
        cur.execute(f"SELECT balance FROM app_{table} WHERE tg_id_id = %s", (tg_id,))
        return cur.fetchone()[0]
    finally:
        cur.close()
        db.close()


async def get_amount(tg_id, transaction_type):
    db, cur = connect()
    try:
        cur.execute("SELECT SUM(amount) FROM app_balancehistory WHERE tg_id_id=%s AND transaction=%s "
                    "AND transaction_type = %s", (tg_id, "IN", transaction_type,))
        refill = cur.fetchone()
        refill = float(refill[0]) if refill[0] else 0
        cur.execute("SELECT SUM(amount) FROM app_balancehistory WHERE tg_id_id=%s AND transaction=%s "
                    "AND transaction_type = %s", (tg_id, "OUT", transaction_type,))
        out = cur.fetchone()
        out = float(out[0]) if out[0] else 0
        return refill, out
    finally:
        cur.close()
        db.close()


async def get_balance_line(tg_id, table):
    db, cur = connect()
    try:
        cur.execute(f"SELECT balance, deposit FROM app_{table} WHERE tg_id_id=%s", (tg_id,))
        result = cur.fetchone()
        return result
    finally:
        cur.close()
        db.close()


async def balance_to_deposit_autoreinvest(table):
    db, cur = connect()
    try:
        if table == "balance":
            account = "Коллективный аккаунт"
        else:
            account = "Стабилизационный пул"
        cur.execute("SELECT tg_id_id FROM app_balance WHERE settings is NULL OR settings = 100")
        tg_ids = [user[0] for user in cur.fetchall()]
        for tg_id in tg_ids:
            balance = await get_my_balance(tg_id, table)
            cur.execute(f"UPDATE app_{table} SET deposit = deposit + %s, "
                        "balance = %s WHERE tg_id_id = %s", (float(round(balance, 2)), 0.0, tg_id,))
            db.commit()
        cur.execute("SELECT tg_id_id FROM app_balance WHERE settings = 0")
        tg_ids = [user[0] for user in cur.fetchall()]
        for tg_id in tg_ids:
            refill, out = await get_amount(tg_id, account)
            body = refill - out
            balance_, deposit_ = await get_balance_line(tg_id, table)
            full_balance = float(balance_) + float(deposit_)
            income = full_balance - body
            cur.execute(f"UPDATE app_{table} SET deposit = deposit + %s, "
                        "balance = %s WHERE tg_id_id = %s", (float(round(body, 2)), income, tg_id,))
            db.commit()
        cur.execute("SELECT tg_id_id FROM app_balance WHERE settings = 50")
        tg_ids = [user[0] for user in cur.fetchall()]
        for tg_id in tg_ids:
            refill, out = await get_amount(tg_id, account)
            body = refill - out
            balance_, deposit_ = await get_balance_line(tg_id, table)
            full_balance = float(balance_) + float(deposit_)
            income = (full_balance - body) / 2
            body = body + income
            cur.execute(f"UPDATE app_{table} SET deposit = deposit + %s, "
                        "balance = %s WHERE tg_id_id = %s", (float(round(body, 2)), income, tg_id,))
            db.commit()
    finally:
        cur.close()
        db.close()


async def transfer_deposit_to_balance():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id_id FROM app_balance")
        tg_ids = [user[0] for user in cur.fetchall()]
        for tg_id in tg_ids:
            cur.execute("SELECT deposit FROM app_balance WHERE tg_id_id = %s", (tg_id,))
            deposit = cur.fetchone()[0]
            cur.execute("UPDATE app_balance SET balance = balance + %s, deposit = 0 WHERE tg_id_id = %s",
                        (deposit, tg_id,))
        db.commit()
    finally:
        cur.close()
        db.close()


async def get_balance_status(tg_id, table):
    db, cur = connect()
    try:
        cur.execute(f"SELECT * FROM app_{table} WHERE tg_id_id=%s", (tg_id,))
        result = cur.fetchone()
        return result
    finally:
        cur.close()
        db.close()


async def add_weekly_profit(weekly_profit, tg_id, table):
    db, cur = connect()
    try:
        cur.execute(f"UPDATE app_{table} SET weekly_profit = %s WHERE tg_id_id = %s", (weekly_profit, tg_id,))
        db.commit()
    finally:
        db.close()
        cur.close()


async def get_inviter_id(tg_id, line):
    db, cur = connect()
    try:
        cur.execute(f"SELECT tg_id_id FROM app_referral WHERE line_{line}=%s", (tg_id,))
        result = cur.fetchone()
        return result
    finally:
        db.close()
        cur.close()


async def get_line(tg_id, line):
    db, cur = connect()
    try:
        cur.execute(f"SELECT line_{line} FROM app_referral WHERE tg_id_id=%s AND line_{line} IS NOT NULL", (tg_id,))
        result = [tg_id[0] for tg_id in cur.fetchall()]
        amount = len(result)
        return amount, result
    finally:
        db.close()
        cur.close()


async def update_referral_profit(tg_id, profit):
    db, cur = connect()
    try:
        cur.execute("UPDATE app_balance SET balance = balance + %s, referral_balance = referral_balance + %s "
                    "WHERE tg_id_id = %s",
                    (profit, profit, tg_id,))
        db.commit()
    finally:
        cur.close()
        db.close()


async def update_weekly_deposit(tg_id, weekly_profit, table):
    db, cur = connect()
    try:
        cur.execute(f"UPDATE app_{table} SET deposit = deposit + %s WHERE tg_id_id = %s", (weekly_profit, tg_id,))
        db.commit()
    finally:
        cur.close()
        db.close()


async def count_users_profit_collective(profit_percentage):
    tg_ids = await get_all_tg_id()
    for tg_id in tg_ids:
        deposit = await get_balance_status(tg_id, 'balance')
        weekly_profit = 0
        try:
            deposit_ = deposit[2]
        except TypeError:
            deposit_ = 0
        if deposit_ < 75000:
            if deposit_ == 0:
                pass
            elif deposit_ < 5000:
                weekly_profit = deposit_ * (profit_percentage / 100) * 0.4
            elif 5000 <= deposit_ < 15000:
                weekly_profit = deposit_ * (profit_percentage / 100) * 0.45
            elif deposit_ >= 15000:
                weekly_profit = deposit_ * (profit_percentage / 100) * 0.5
            await add_weekly_profit(weekly_profit, tg_id, 'balance')
            line_3 = await get_inviter_id(tg_id, '3')
            line_2 = await get_inviter_id(tg_id, '2')
            line_1 = await get_inviter_id(tg_id, '1')
            referral_percentage = deposit_ * (profit_percentage / 100)
            try:
                if line_1[0]:
                    referral_profit_1 = round(referral_percentage * 0.05, 2)
                    await update_referral_profit(line_1[0], referral_profit_1)
            except TypeError:
                pass
            try:
                if line_2[0]:
                    referral_profit_2 = round(referral_percentage * 0.03, 2)
                    await update_referral_profit(line_2[0], referral_profit_2)
            except TypeError:
                pass
            try:
                if line_3[0]:
                    referral_profit_3 = round(referral_percentage * 0.02, 2)
                    await update_referral_profit(line_3[0], referral_profit_3)
            except TypeError:
                pass


async def count_users_profit_stabpool(profit_percentage):
    tg_ids = await get_all_tg_id()
    for tg_id in tg_ids:
        deposit = await get_balance_status(tg_id, 'stabpool')
        try:
            deposit_ = deposit[2]
        except TypeError:
            deposit_ = 0
        weekly_profit = deposit_ * (profit_percentage[0] / 100) * 0.6
        await add_weekly_profit(weekly_profit, tg_id, 'stabpool')
        bot = Bot(token=config("BOT_TOKEN"))
        session = await bot.get_session()
        try:
            if deposit_ == 0:
                await session.close()
            else:
                print(tg_id)
                await bot.send_message(
                    chat_id=tg_id,
                    text=f"<b>📨 [Стабилизационный пул] Отчет на {datetime.now().date().strftime('%d.%m.%Y')}</b>"
                         f"\n\n<em>💰 Ваша доходность за торговую неделю:"
                         f"</em> {round(weekly_profit, 2)} USDT"
                         f"<em>\n\n📈 Общий профит J2M:</em> {round(profit_percentage[0], 2)} %"
                         f"\n\n\n<em>Баланс будет обновлен в течение суток!"
                         f"Возможны незначительные отличия партнерских начислений "
                         f"в отчете от реальных (в пределах 1%)</em>"
                         f"\n\n<a href='https://telegra.ph/Kak-vyschityvaetsya-dohodnost-polzovatelya-J2M-07-21-2'>"
                         f"Подробнее о правилах начисления доходности</a>",
                    parse_mode=types.ParseMode.HTML)
                await session.close()
        except BotBlocked:
            await bot.send_message(chat_id=config("GROUP_ID"),
                                   text=f"Пользователь с ID {tg_id} заблокировал бота!")
            await session.close()


async def send_message_with_profit_collective(profit_percentage):
    all_tg_ids = await get_all_tg_id()
    for tg_id in all_tg_ids:
        user_data = await get_balance_status(tg_id, 'balance')
        try:
            weekly_profit = user_data[8] if user_data[8] is not None else 0
        except TypeError:
            weekly_profit = 0
        line_1_ids = await get_line(tg_id, '1')
        line_2_ids = await get_line(tg_id, '2')
        line_3_ids = await get_line(tg_id, '3')
        referral_profit_line1 = 0
        referral_profit_line2 = 0
        referral_profit_line3 = 0
        ref_x = 0
        ref_x2 = 0
        ref_x3 = 0
        if line_1_ids:
            for line_1_id in line_1_ids[1]:
                referral_profit_line1_data = await get_balance_status(line_1_id, 'balance')
                if referral_profit_line1_data is not None:
                    count = 0.45
                    ref_x += referral_profit_line1_data[2]
                    if referral_profit_line1_data[2] < 5000:
                        count = 0.4
                    if referral_profit_line1_data[2] > 15000:
                        count = 0.5
                    try:
                        referral_profit_line1 += float(referral_profit_line1_data[
                                                           8] / count) * 0.05 if referral_profit_line1_data is not None else 0
                    except TypeError:
                        referral_profit_line1 += 0
        if line_2_ids:
            for line_2_id in line_2_ids[1]:
                referral_profit_line2_data = await get_balance_status(line_2_id, 'balance')
                if referral_profit_line2_data is not None:
                    count = 0.45
                    ref_x2 += referral_profit_line2_data[2]
                    if referral_profit_line2_data[2] < 5000:
                        count = 0.4
                    if referral_profit_line2_data[2] > 15000:
                        count = 0.5
                    try:
                        referral_profit_line2 += float(referral_profit_line2_data[
                                                           8] / count) * 0.03 if referral_profit_line2_data is not None else 0
                    except TypeError:
                        referral_profit_line2 += 0

        if line_3_ids:
            for line_3_id in line_3_ids[1]:
                referral_profit_line3_data = await get_balance_status(line_3_id, 'balance')
                if referral_profit_line3_data is not None:
                    ref_x3 += referral_profit_line3_data[2]
                    count = 0.45
                    if referral_profit_line3_data[2] < 5000:
                        count = 0.4
                    if referral_profit_line3_data[2] > 15000:
                        count = 0.5
                    try:
                        referral_profit_line3 += (referral_profit_line3_data[
                                                      8] / count) * 0.02 if referral_profit_line3_data is not None else 0
                    except TypeError:
                        referral_profit_line3 += 0

        bot = Bot(token=config("BOT_TOKEN"))
        session = await bot.get_session()
        try:
            if weekly_profit > 0 or referral_profit_line1 > 0 or referral_profit_line2 > 0 or referral_profit_line3 > 0:
                print(f"{tg_id} - "
                      f"WP: {weekly_profit} "
                      f"- 1 {referral_profit_line1}, "
                      f"2 {referral_profit_line2}, "
                      f"3 {referral_profit_line3} -- "
                      f"!{ref_x + ref_x2 + ref_x3}")
                await bot.send_message(
                    chat_id=tg_id,
                    text=f"<b>📨 Отчет на {datetime.now().date().strftime('%d.%m.%Y')}</b>"
                         f"\n\n<em>💰 Ваша доходность за торговую неделю:"
                         f"</em> {round(weekly_profit, 2)} USDT"
                         f"<em>\n\n📈 Общий профит J2M:</em> {round(profit_percentage[0], 2)} %"
                         f"\n\n<em>👨‍👦‍👦 Партнерские начисления:</em>"
                         f"\n   ↳ <em>1 линия (5% от дохода): {round(referral_profit_line1, 2)} USDT </em>"
                         f"\n   ↳ <em>2 линия (3% от дохода): {round(referral_profit_line2, 2)} USDT </em>"
                         f"\n   ↳ <em>3 линия (2% от дохода): {round(referral_profit_line3, 2)} USDT </em>"
                         f"\n   ↳ <em> Общие партнерские начисления: "
                         f"{round(referral_profit_line1 + referral_profit_line2 + referral_profit_line3, 2)} USDT</em>"
                         f"\n\n\n<em>Баланс будет обновлен в течение суток!"
                         f"Возможны незначительные отличия партнерских "
                         f"начислений в отчете от реальных (в пределах 1%)</em>"
                         f"\n\n<a href='https://telegra.ph/Kak-vyschityvaetsya-dohodnost-polzovatelya-J2M-07-21-2'>"
                         f"Подробнее о правилах начисления доходности</a>",
                    parse_mode=types.ParseMode.HTML)
                await session.close()
            else:
                await bot.send_message(
                    chat_id=tg_id,
                    text=f"<b>📨 Отчет на {datetime.now().date().strftime('%d.%m.%Y')}</b>"
                         f"\n\n<em>💰 Ваша доходность за торговую неделю:"
                         f"</em> Вы не участвовали в торговой неделе. Измените процент "
                         f"реинвестирования и/или пополните баланс!"
                         f"<em>\n\n📈 Общий профит J2M:</em> {round(profit_percentage[0], 2)} %"
                         f"\n\n\n<em>Баланс будет обновлен в течение суток!</em>"
                         f"\n\n<a href='https://telegra.ph/Kak-vyschityvaetsya-dohodnost-polzovatelya-J2M-07-21-2'>"
                         f"Подробнее о правилах начисления доходности</a>",
                    parse_mode=types.ParseMode.HTML)
                await session.close()
        except BotBlocked:
            await bot.send_message(chat_id=config("GROUP_ID"),
                                   text=f"Пользователь с ID {tg_id} заблокировал бота!")
            await session.close()


async def weekly_deposit_update():
    tg_ids = await get_all_tg_id()
    for tg_id in tg_ids:
        try:
            weekly_deposit = await get_balance_status(tg_id, "balance")
            if weekly_deposit[8] != 0 and weekly_deposit[4] == 0:
                await update_weekly_deposit(tg_id, round(weekly_deposit[8], 2), 'balance')
        except TypeError:
            pass
        try:
            weekly_deposit_stabpool = await get_balance_status(tg_id, "stabpool")
            if weekly_deposit_stabpool[5] != 0:
                await update_weekly_deposit(tg_id, round(weekly_deposit_stabpool[5], 2), 'stabpool')
        except TypeError:
            pass
