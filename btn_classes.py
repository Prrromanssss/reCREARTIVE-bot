import datetime as dt
import json
from random import choice

import psycopg2
import pytz
from pytz import timezone
from telebot import types
from tzwhere import tzwhere as tz

from settings import CHAT_ID_MODERATE, DB_TABLE_NAME, DBI_URI


class Notify:
    def __init__(self):
        self.flag_for_sending = {}
        self.already_get = {}
        self.flag_location = {}

    async def notify_settings(self, bot, message):
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton('/notify'))
        markup.add(types.KeyboardButton('/exist_notify'))
        await bot.send_message(
            message.chat.id,
            'Вы хотите настроить уведомления или узнать о существующих?',
            reply_markup=markup
            )
        await stick.send_stickers(bot, message)

    async def existing_notifies(self, bot, message):
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton('no'))
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''SELECT time
                                  FROM {DB_TABLE_NAME}
                                  WHERE user_id = %s
                               '''
        cursor.execute(sqlite_select_query, (message.chat.id,))
        time = cursor.fetchone()[0]
        if not time:
            await bot.send_message(
                message.chat.id,
                'У вас не выставлены никакие уведомления.'
                ' Давайте это исправим!'
                )
            await self.local_time(bot, message)
        else:
            markup = init_btns()
            time = "".join(time.split()[-1]).split(":")
            await bot.send_message(
                message.chat.id,
                f'Уведомления выставлены на: {time[0]}:{time[1]}',
                reply_markup=markup
                )
            await stick.send_stickers(bot, message)

    async def local_time(self, bot, message):
        self.flag_location[message.chat.id] = True
        conn = psycopg2.connect(DBI_URI, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''SELECT *
                                  FROM {DB_TABLE_NAME}
                                  WHERE user_id = %s
                               '''
        db_conn.stack_write_db_task[message.chat.id] = False
        cursor.execute(sqlite_select_query, (message.chat.id,))
        markup = types.ReplyKeyboardRemove()
        text = ('Пришлите нам свое местоположение. \n\n'
                'P.s.: "скрепка" в левом нижнем углу'
                '(так же, как и фото отправлять)'
                )
        await bot.send_message(message.chat.id, text, reply_markup=markup)
        await stick.send_stickers(bot, message)

    async def turn_on_notif(self, bot, message):
        db_conn.stack_write_db_task[message.chat.id] = False
        self.flag_location[message.chat.id] = True
        markup = types.InlineKeyboardMarkup(row_width=6)
        times = []
        for time in [f'0{i}:00' if i < 10 else f'{i}:00'
                     for i in range(0, 24)]:
            times.append(types.InlineKeyboardButton(
                text=time,
                callback_data=time,
                ))
        markup.add(*(i for i in times))
        self.flag_for_sending[message.chat.id] = True
        await bot.send_message(
            message.from_user.id,
            'Выберите время для отправки сообщений',
            reply_markup=markup,
            )
        await stick.send_stickers(bot, message)

    async def turn_off_notif(self, bot, message):
        db_conn.stack_write_db_task[message.chat.id] = False
        self.flag_for_sending[message.chat.id] = False
        markup = init_btns()
        await bot.send_message(
            message.from_user.id,
            'Супер, уведомления выключены!',
            reply_markup=markup
            )
        await stick.send_stickers(bot, message)


class DataBase:
    def __init__(self, name):
        self.name = name
        self.msgs = {}
        self.stack_write_db_task = {}

    async def db_get_task(self, bot, message):
        chat_id = message if isinstance(message, int) else message.chat.id
        self.stack_write_db_task[chat_id] = False
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''SELECT *
                                  FROM {DB_TABLE_NAME}
                                  WHERE message IS NOT NULL
                                  ORDER BY RANDOM()
                                  LIMIT 1;
                               '''
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        markup = init_btns()
        try:
            surname = records[0][3] if records[0][3] else ''
            user = (
                records[0][4]
                if records[0][4]
                else records[0][2] + ' ' + surname
                )
            text = f'Задание от {user}:\n\n{records[0][5]}'
            conn.commit()

            await bot.send_message(chat_id, text, reply_markup=markup)
            await bot.send_message(chat_id, choice(set_of_funny_msg))
            await stick.send_stickers(bot, chat_id)
        except IndexError:
            await bot.send_message(
                message.chat.id,
                'Задания еще нет\nБудьте первыми, кто его напишет!',
                reply_markup=markup
                )
            await stick.send_stickers(bot, message)

    async def db_before_write_task(self, bot, message):
        self.stack_write_db_task[message.chat.id] = True
        markup = types.ReplyKeyboardRemove()
        await bot.send_message(
            message.chat.id,
            'Напишите ваше задание',
            reply_markup=markup
            )
        await stick.send_stickers(bot, message)

    async def db_write_task(self, bot, message, *args):
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''SELECT *
                                  FROM {DB_TABLE_NAME}
                                  WHERE user_id = %s
                               '''
        user_id = message.from_user.id if not args else args[0]
        cursor.execute(sqlite_select_query, (user_id,))
        records = cursor.fetchall()
        user_name = message.from_user.first_name if not args else args[1]
        user_surname = message.from_user.last_name if not args else args[2]
        username = message.from_user.username if not args else args[3]
        user_msg = message.text if not args else args[4]
        cursor.execute(
            f'''SELECT *
                FROM {DB_TABLE_NAME}
                WHERE user_id = %s AND message IS NULL
                ''',
            (user_id,)
            )
        empty_msg = cursor.fetchall()
        if empty_msg:
            val = (user_msg, user_id)

            cursor.execute(
                f'''UPDATE {DB_TABLE_NAME}
                    SET message = %s
                    WHERE user_id = %s'
                    AND message IS NULL''',
                val,
                )
        elif records:
            utc = records[0][-2]
            time = (
                dt.datetime(*map(int, ''.join(records[0][-1].split()[0])
                            .split('-')),
                            *map(int, ''.join(records[0][-1].split()[1])
                            .split(':'))).strftime('%Y-%m-%d %H:%M:%S')
                    )
            val = (
                user_id,
                user_name,
                user_surname,
                username,
                user_msg,
                utc,
                time
                )
            cursor.execute(
                f'''INSERT INTO {DB_TABLE_NAME}
                        (user_id, "user_name",
                        "user_surname", "username",
                        "message", utc, time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''',
                val
                )
        else:
            val = (user_id, user_name, user_surname, username, user_msg)
            cursor.execute(
                f'''INSERT INTO {DB_TABLE_NAME}
                        (user_id, "user_name", "user_surname",
                        "username", "message")
                    VALUES
                        (%s, %s, %s, %s, %s)''',
                val
                )

        conn.commit()
        self.stack_write_db_task[user_id] = False
        markup = init_btns()
        await bot.send_message(
            user_id,
            'Успешно! Ваше задание было добавлено в общую базу данных\n\n'
            f'<strong>Задание:\n</strong>{user_msg} ',
            reply_markup=markup, parse_mode='html'
            )
        await stick.send_stickers(bot, user_id)

    async def db_set_time(self, bot, message, data):
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        sqlite_select_query = f'''SELECT *
                                  FROM {DB_TABLE_NAME}
                                  WHERE user_id = %s
                               '''
        cursor.execute(sqlite_select_query, (message.chat.id,))

        utc = int(cursor.fetchall()[0][-2])
        differ_time = dt.timedelta(hours=abs(utc))
        dt_now = dt.datetime.now(timezone('Europe/Moscow'))
        dt_now = dt.datetime(
            year=dt_now.year,
            month=dt_now.month,
            day=dt_now.day,
            hour=int(data.split(':')[0]),
            minute=int(data.split(':')[1])
            )
        if utc >= 0:
            dt_time = dt_now + differ_time
        else:
            dt_time = dt_now - differ_time
        dt_time = dt_time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            f'UPDATE {DB_TABLE_NAME} SET time = %s WHERE user_id = %s',
            (dt_time, message.chat.id)
            )
        conn.commit()
        markup = init_btns()
        text = 'Время выставлено: ' + data
        await bot.send_message(message.chat.id, text, reply_markup=markup)
        await stick.send_stickers(bot, message)

    async def db_update_task(self, bot, message):
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        lng = message.location.longitude
        lat = message.location.latitude
        tzwhere = tz.tzwhere()
        timezone_str = tzwhere.tzNameAt(lat, lng)
        timezone_str = pytz.timezone(timezone_str)
        differ_int = (int(dt.datetime.now
                      (timezone_str).hour - dt.datetime.now
                      (timezone('Europe/Moscow')).hour)
                      )
        sqlite_select_query = f'''SELECT *
                                  FROM {DB_TABLE_NAME}
                                  WHERE user_id = %s
                               '''
        cursor.execute(sqlite_select_query, (message.chat.id,))
        if not cursor.fetchall():
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            user_surname = message.from_user.last_name
            username = message.from_user.username
            sqlite_insert_query = f'''INSERT INTO {DB_TABLE_NAME}
                                          (user_id, "user_name",
                                          "user_surname", "username")
                                      VALUES'
                                          (%s, %s, %s, %s)
                                   '''
            cursor.execute(
                sqlite_insert_query,
                (user_id, user_name, user_surname, username)
                )
        cursor.execute(
            f'UPDATE {DB_TABLE_NAME} SET utc = %s WHERE user_id = %s',
            (differ_int, message.chat.id)
            )
        conn.commit()
        await bot.send_message(message.chat.id, 'Ваша геопозиция обновлена!')
        await notifies.turn_on_notif(bot, message)

    async def db_before_confirm_task(self, bot, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('/confirm')
        btn2 = types.KeyboardButton('/not_confirm')
        markup.add(btn1, btn2)
        text = f'Подтвердите задание.\nВаше задание:\n\n{message.text}'
        await bot.send_message(message.chat.id, text, reply_markup=markup)
        await stick.send_stickers(bot, message)

    async def db_confirm_task(self, bot, message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        user_surname = message.from_user.last_name
        username = message.from_user.username
        markup = init_btns()
        await bot.send_message(
            message.chat.id,
            'Ваше задание отправлено модераторам на проверку',
            reply_markup=markup
            )
        await stick.send_stickers(bot, message)
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(
            text='Подтвердить',
            callback_data='Подтвердить'
            )
        btn2 = types.InlineKeyboardButton(
            text='Не подтвердить',
            callback_data='Не подтвердить'
            )
        markup.add(btn1, btn2)
        await bot.send_message(
            CHAT_ID_MODERATE,
            f'Сообщение от\nuser_id: {user_id}\nuser_name: {user_name}\n'
            f'user_surname: {user_surname}\nusername: {username}\n'
            f'<strong>Задание</strong>: {self.msgs[message.chat.id].text}\n'
            f'<strong>Статус:</strong> на проверке',
            reply_markup=markup, parse_mode='html'
            )

    async def db_not_confirm_task(self, bot, message):
        markup = init_btns()
        text = 'Попробуйте позже, мы будем вас ждать :)\n'
        text += ('Для того, чтобы записать задание ещё раз,'
                 'нажмите кнопку "write_task" и повторите алгоритм')
        await bot.send_message(message.chat.id, text, reply_markup=markup)
        await stick.send_stickers(bot, message)


class Stickers:
    def __init__(self):
        self.flag = {}
        self.stick_sending = {}

    async def send_stickers(self, bot, message):
        chat_id = message if isinstance(message, int) else message.chat.id
        data = open_file('data_stick.json')

        if data and str(chat_id) in data and data[str(chat_id)]:
            await bot.send_sticker(
                chat_id,
                choice(list(data[str(chat_id)].values()))
                )

    async def turn_stick(self, bot, message):
        db_conn.stack_write_db_task[message.chat.id] = False
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('/add_stickers')
        btn2 = types.KeyboardButton('/del_stickers')
        markup.add(btn1, btn2)
        await bot.send_message(
            message.from_user.id,
            'Вы хотите пополнить стикеры или удалить ?',
            reply_markup=markup
            )
        await self.send_stickers(bot, message)

    async def add_del(self, bot, message):
        db_conn.stack_write_db_task[message.chat.id] = False
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('/stop_stickers')
        markup.add(btn1)
        await bot.send_message(
            message.from_user.id,
            'Присылайте стикеры, как закончите нажмите кнопку '
            '"/stop_stickers".\nЕсли у вас не работает кнопка выбора стикеров'
            ' на клавиатуре ввода, пришлите их нам с компьютера. '
            'Такая проблема может возникать на iPhone',
            reply_markup=markup,
            )
        await self.send_stickers(bot, message)

    async def add_stick(self, bot, message):
        self.stick_sending[message.chat.id] = True
        db_conn.stack_write_db_task[message.chat.id] = False
        self.flag[message.chat.id] = True
        await self.add_del(bot, message)

    async def del_stick(self, bot, message):
        self.stick_sending[message.chat.id] = True
        db_conn.stack_write_db_task[message.chat.id] = False
        self.flag[message.chat.id] = False
        await self.add_del(bot, message)

    async def stop_stick(self, bot, message):
        markup = init_btns()
        db_conn.stack_write_db_task[message.chat.id] = False
        if self.stick_sending[message.chat.id]:
            await bot.send_message(
                message.from_user.id,
                'Ваш набор стикеров обновился!',
                reply_markup=markup
                )
        else:
            await bot.send_message(
                message.from_user.id,
                'Эта кнопка действуют только после "add_stickers" и'
                ' "del_stickers"'
                )
        await self.send_stickers(bot, message)
        self.stick_sending[message.chat.id] = False


def open_file(json_file):
    try:
        with open(json_file) as file:
            data = json.loads(file.read())
    except json.decoder.JSONDecodeError:
        data = {}
    return data


def init_btns():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('/write_task')
    btn2 = types.KeyboardButton('/get_task')
    btn3 = types.KeyboardButton('/notify_settings')
    btn4 = types.KeyboardButton('/not_notify')
    btn5 = types.KeyboardButton('/stickers')
    btn6 = types.KeyboardButton('/help')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup


db_conn = DataBase(DBI_URI)
stick = Stickers()
notifies = Notify()
set_of_funny_msg = ['Удачи в выполнении!', 'Надеюсь у тебя все получится!',
                    'Ни пуха ни пера!', 'Хорошо покреативить!',
                    'С Богом!', 'Да прибудет с тобой сила!',
                    'В добрый час :)', 'Хорошего дня!',
                    'Ты справишься!', 'Увидимся завтра :)'
                    ]
