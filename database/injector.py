import datetime

import psycopg2
from decouple import config

team_accounts = [835895834, 15362825, 468156477, 165030749, 6159712492, 6258470703, 254465569, 1350441479, 149019824]
ad_accounts = [340862178, 452517420, 248745860]
test_accounts = [361957627]


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
    except psycopg2.Error:
        db = psycopg2.connect(
            host=config("DB_HOST"),
            database=config("DB_NAME"),
            user=config("DB_USER"),
            password=config("DB_PASSWORD")
        )
        cur = db.cursor()
        return db, cur


async def j2m_balance_data():
    db, cur = connect()
    try:
        cur.execute("SELECT date_monday, balance_monday_usdt, balance_monday_busd, date_sunday,"
                    " balance_sunday_usdt, balance_sunday_busd, profit FROM app_balancej2m")
        rows = cur.fetchall()
        new_data = [(row[0].strftime('%d.%m.%Y'), row[1], row[2],
                     row[3].strftime('%d.%m.%Y') if row[3] else 'Нет данных', row[4], row[5], row[6]) for row in rows]
        return new_data
    finally:
        cur.close()
        db.close()


async def balancehistory_data():
    db, cur = connect()
    try:
        cur.execute("SELECT date, tg_id_id, transaction, amount FROM app_balancehistory")
        rows = cur.fetchall()
        data_with_formatted_date = [
            (row[0].strftime('%d.%m.%Y'), row[1], "Пополнение" if row[2] == "IN" else "Вывод", row[3],
             "Рекламный" if row[1] in ad_accounts or team_accounts or test_accounts else "Реальный") for row in rows
        ]
        return data_with_formatted_date
    finally:
        cur.close()
        db.close()


async def j2m_users_data():
    db, cur = connect()
    now = datetime.datetime.now().date().strftime('%d.%m.%Y')
    try:
        cur.execute("SELECT tg_id, tg_username, tg_name, language, alias, wallet, email FROM app_j2muser")
        user_rows = cur.fetchall()
        cur.execute("SELECT tg_id_id, name, social FROM app_form")
        form_rows = cur.fetchall()
        form_data = {row[0]: {'name': row[1], 'social': row[2]} for row in form_rows}
        combined_data = []
        for user_row in user_rows:
            tg_id = user_row[0]
            name = form_data.get(tg_id, {}).get('name', "")
            social = form_data.get(tg_id, {}).get('social', "")
            combined_data.append([
                now, str(tg_id), user_row[1], user_row[2], user_row[3], user_row[4] if user_row[4] else 'Нет данных',
                user_row[5] if user_row[5] else 'Кошелька нет', user_row[6], name if name else 'Нет данных',
                social if social else 'Нет данных'])
        return combined_data
    finally:
        cur.close()
        db.close()


async def nft_data():
    db, cur = connect()
    try:
        cur.execute("SELECT date, tg_id_id, status FROM app_nft")
        rows = cur.fetchall()
        data_with_formatted_date = [(row[0].strftime('%d.%m.%Y'), row[1],
                                     row[2] if row[2] else "Пользователь не приобрёл NFT") for row in rows]
        return data_with_formatted_date
    finally:
        cur.close()
        db.close()


async def balance_data():
    db, cur = connect()
    now = datetime.datetime.now().date().strftime('%d.%m.%Y')
    try:
        cur.execute("SELECT tg_id_id, balance, deposit, withdrawal, referral_balance, "
                    "hold, settings, weekly_profit FROM app_balance")
        rows = cur.fetchall()
        new_data = []
        for row in rows:
            tg_id = row[0]
            status = 'Реальный аккаунт'
            if tg_id in team_accounts:
                status = 'Команда'
            elif tg_id in ad_accounts:
                status = 'Реклама'
            elif tg_id in test_accounts:
                status = 'Тестировщик'
            cur.execute('SELECT * FROM app_balancehistory WHERE tg_id_id = %s '
                        'AND transaction = %s', (tg_id, "IN"))
            result = cur.fetchone()
            first_withdrawal_date = result[2] if result else None
            new_row = (
                now, row[0], status, row[1], row[2], row[3], row[4],
                row[5] if row[5] else 'Пополнение юзера менее 1000',
                first_withdrawal_date.strftime('%d.%m.%Y') if first_withdrawal_date else 'Нет данных',
                row[6], row[7] if row[7] else 0)
            new_data.append(new_row)
        return new_data
    finally:
        cur.close()
        db.close()


async def stabpool_data():
    db, cur = connect()
    now = datetime.datetime.now().date().strftime('%d.%m.%Y')
    try:
        cur.execute("SELECT tg_id_id, balance, deposit, withdrawal, hold, weekly_profit FROM app_stabpool")
        rows = cur.fetchall()
        new_data = []
        for row in rows:
            tg_id = row[0]
            cur.execute("SELECT date FROM app_balancehistory WHERE tg_id_id = %s "
                        "AND transaction = %s AND transaction_type = %s ORDER BY date LIMIT 1",
                        (tg_id, "IN", "Стабилизационный пул"))
            result = cur.fetchone()
            first_transaction = result[0] if result else None
            if first_transaction:
                new_row = (now, row[0], row[1], row[2], row[3], row[4], first_transaction.strftime('%d.%m.%Y'),
                           row[5] if row[5] else 0)
                new_data.append(new_row)
        return new_data
    finally:
        cur.close()
        db.close()


async def demo_data():
    db, cur = connect()
    now = datetime.datetime.now().date().strftime('%d.%m.%Y')
    try:
        cur.execute("SELECT tg_id_id, balance_collective, deposit_collective FROM demo_demouser")
        rows = cur.fetchall()
        new_data = []
        for row in rows:
            new_row = (now, row[0], row[1], row[2])
            new_data.append(new_row)
        return new_data
    finally:
        cur.close()
        db.close()
