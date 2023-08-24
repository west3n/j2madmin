import asyncio
import datetime

from google_sheets import old_data


async def j2m_balance_sheets():
    now = datetime.datetime.now()
    print(f"Запущена ежедневная задача j2m_balance_sheets\nВремя запуска: {now.strftime('%Y-%m-%d %H:%M')}")
    while True:
        if now.weekday() == 1 and now.hour == 0 and now.minute == 10:
            print(f"Выполняется задача по добавлению новых записей в Google Sheets."
                  f"\n\nДата: {now.date()}")
            await old_data.balance_j2m_sheets()
            print(f"Запись баланса J2M прошла успешно!")
            await old_data.balance_sheets()
            print(f"Запись баланса пользователей прошла успешно!")
            await old_data.stabpool_sheets()
            print(f"Запись пользователей стабилизационного пула прошла успешно!")
        if now.hour == 0 and now.minute == 30:
            print(f"Выполняется задача по добавлению новых записей в Google Sheets."
                  f"\n\nДата: {now.date()}")
            await old_data.j2musers_sheets()
            print(f"Запись пользователей J2M прошла успешно!")
        await asyncio.sleep(60 - now.second)


if __name__ == '__main__':
    asyncio.run(j2m_balance_sheets())
