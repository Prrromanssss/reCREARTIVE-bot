import btn_classes
import psycopg2
import asyncio
from main import bot
import datetime as dt
from config_data import DBI_URI, DB_TABLE_NAME

date = btn_classes.dt.datetime.now(btn_classes.timezone('Europe/Moscow'))


async def try_send_schedule():
    while True:
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'SELECT DISTINCT user_id, utc, time FROM {DB_TABLE_NAME} ;'
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        conn.commit()
        for user in records:
            if (user[-1] and user[0] in btn_classes.notifies.flag_for_sending
                    and btn_classes.notifies.flag_for_sending[user[0]]
                    and (user[0] not in btn_classes.notifies.already_get or btn_classes.notifies.already_get[user[0]])):
                dt_now = dt.datetime.now(btn_classes.timezone('Europe/Moscow'))
                dt_need_hour = int(user[-1].split()[-1][:2][1] if not int(user[-1].split()[-1][:2][0])
                                   else user[-1].split()[-1][:2])
                dt_need_min = int(user[-1].split()[-1][3:5][1] if not int(user[-1].split()[-1][:2][0])
                                  else user[-1].split()[-1][3:5])

                if user[1] >= 0:
                    if ((dt_now + dt.timedelta(user[1])).hour == dt_need_hour
                            and (dt_now + dt.timedelta(user[1])).minute == dt_need_min):
                        await btn_classes.db_conn.db_get_task(bot, user[0])
                        btn_classes.notifies.already_get[user[0]] = False
                else:
                    if ((dt_now - dt.timedelta(user[1])).hour == dt_need_hour
                            and (dt_now - dt.timedelta(user[1])).minute == dt_need_min):
                        await btn_classes.db_conn.db_get_task(bot, user[0])
                        btn_classes.notifies.already_get[user[0]] = False
        await asyncio.sleep(1)


async def update_sch():
    global date
    while True:
        date_now = dt.datetime.now(btn_classes.timezone('Europe/Moscow'))
        if not (date_now - date).days:
            date = dt.datetime.now(btn_classes.timezone('Europe/Moscow'))
            for user in btn_classes.notifies.already_get:
                btn_classes.notifies.already_get[user] = True

        await asyncio.sleep(3600)