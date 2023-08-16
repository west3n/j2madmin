import asyncio
import datetime

from google_sheets import old_data


async def j2m_balance_sheets():
    while True:
        now = datetime.datetime.now()
        if now.weekday() == 1 and now.hour == 0 and now.minute == 10:
            print("Выполняется задача по добавлению новых записей в Google Sheets")
            await old_data.balance_j2m_sheets()
            await old_data.balance_sheets()
        if now.hour == 0 and now.minute == 30:
            await old_data.j2musers_sheets()
        await asyncio.sleep(60 - now.second)


if __name__ == '__main__':
    asyncio.run(j2m_balance_sheets())
