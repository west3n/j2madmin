import asyncio

import gspread

from decouple import config
from oauth2client.service_account import ServiceAccountCredentials
from database import injector


async def sheets_connection():
    sheet_url = config("SHEET_URL")
    credentials_path = "j2m-project-395212-6143ef593cd0.json"
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    gc = gspread.authorize(credentials)
    sh = gc.open_by_url(sheet_url)
    return sh


async def balance_j2m_sheets():
    sh = await sheets_connection()
    worksheet_name = "Сумма торгового пула"
    worksheet = sh.worksheet(worksheet_name)
    j2m_balance_data = await injector.j2m_balance_data()
    existing_dates = worksheet.col_values(1)[1:]
    for row_data in j2m_balance_data:
        date_value = row_data[0]
        if date_value not in existing_dates:
            worksheet.append_row(row_data)
        else:
            print(f"Запись с датой {date_value} уже существует в таблице!")


async def balancehistory_sheets():
    sh = await sheets_connection()
    worksheet_name = "Сумма пополнения пула"
    worksheet = sh.worksheet(worksheet_name)
    balancehistory_data = await injector.balancehistory_data()
    for row_data in balancehistory_data:
        worksheet.append_row(row_data)


async def j2musers_sheets():
    sh = await sheets_connection()
    worksheet_name = "Пользователи"
    worksheet = sh.worksheet(worksheet_name)
    j2musers_data = await injector.j2m_users_data()
    existing_ids = worksheet.col_values(2)[1:]
    for row_data in j2musers_data:
        tg_id = row_data[1]
        if tg_id in existing_ids:
            row_number = existing_ids.index(tg_id) + 2
            existing_row = worksheet.row_values(row_number)
            existing_row = [str(value) for value in existing_row]
            if existing_row != row_data:
                print("Данные для пользователя с ID", tg_id, "были обновлены:")
                worksheet.update(f"A{row_number}", [row_data])
        else:
            worksheet.append_row(row_data)
            print("Добавлена новая запись для пользователя с ID", tg_id)


async def nft_sheets():
    sh = await sheets_connection()
    worksheet_name = "NFT"
    worksheet = sh.worksheet(worksheet_name)
    nft_data = await injector.nft_data()
    for row_data in nft_data:
        worksheet.append_row(row_data)


async def balance_sheets():
    sh = await sheets_connection()
    worksheet_name = "Доход пользователя"
    worksheet = sh.worksheet(worksheet_name)
    balance_data = await injector.balance_data()
    for row_data in balance_data:
        worksheet.append_row(row_data)


async def stabpool_sheets():
    sh = await sheets_connection()
    worksheet_name = "Стабпул пользователи"
    worksheet = sh.worksheet(worksheet_name)
    balance_data = await injector.stabpool_data()
    for row_data in balance_data:
        worksheet.append_row(row_data)
