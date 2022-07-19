import asyncio
import telebot.async_telebot
import json
import config_data
import btn_classes
import timer
from telebot import types

bot = telebot.async_telebot.AsyncTeleBot(config_data.token)


useful_msg = {'/get_task': btn_classes.db_conn.db_get_task,
              '/write_task': btn_classes.db_conn.db_before_write_task,
              '/confirm': btn_classes.db_conn.db_confirm_task,
              '/not_confirm': btn_classes.db_conn.db_not_confirm_task,
              '/notify': btn_classes.notifies.local_time,
              '/not_notify': btn_classes.notifies.turn_off_notif,
              '/stickers': btn_classes.stick.turn_stick,
              '/add_stickers': btn_classes.stick.add_stick,
              '/del_stickers': btn_classes.stick.del_stick,
              '/stop_stickers': btn_classes.stick.stop_stick
              }


@bot.message_handler(commands=['start', 'help'], chat_types=['private'])
async def main_commands(message):
    markup = btn_classes.init_btns()
    btn_classes.notifies.flag_location[message.chat.id] = False
    btn_classes.stick.flag[message.from_user.id] = None
    greeting = 'Привет, тебя встречает команда reCREARTIVE \n\n'\
               'Мы создали бота, который будет тренировать твою креативность и делиться с тобой взглядом' \
               ' на мир разных художников.\n\n'\
               'Решай задания или просто посмотри на мир так, как это делали разные художники, а потом' \
               ' попробуй воспользоваться их методами.\n\n'\
               'Нажимай кнопку, чтобы получить задание на день или придумай свое и напиши его нам.\n'\
               'Кто знает, кому оно попадется  :)\n\n'\
               'Так же, если вы хотите получать каждый день новое задание '\
               'просто нажмите кнопку "notify", и вы будете становиться креативными каждый день\n\n'\
               'Кстати, можешь накидать нам любимых стикеров, чтобы наше общение было веселее!\n\n'\
               'Выбирай!\n\n'\
               '<strong>Задание</strong>\n'\
               '/get_task - получить задание\n'\
               '/write_task - прислать задание, которое получит другой участник\n'\
               '/confirm - подтвердить задание (а вдруг вы ошиблись :) )\n'\
               '/not_confirm - отменить запись задания (и вправду ошиблись :( )\n' \
               '"confirm" и "not_confirm" используются после кнопки "write_task".\n\n' \
               '<strong>Уведомления</strong>\n' \
               '/notify - настроить уведомления (ты же не хочешь, чтобы мы тебя разбудили? настрой' \
               ' часовой пояс и время отправки уведомлений)\n'\
               '/not_notify - выключить уведомления (после этого уведомления будут выключены)\n\n' \
               '<strong>Стикеры</strong>\n' \
               '/stickers - настроить любимые стикеры (данные стикеры будут приходить вместе'\
               ' с остальными сообщениями)\n'\
               '/add_stickers - добавить стикеры (после нажатия данной кнопки, стикеры будут добавлены'\
               ' в вашу коллекцию)\n'\
               '/del_stickers - удалить стикеры (когда они тебе надоели)\n' \
               '/stop_stickers - остановить отправку стикеров (когда хочется поговорить серьезнее)\n'\
               'Используется после кнопок "add_stickers" и "del_stickers".\n\n'\
               '/help - помощь (узнать доступные команды)\n\n'

    await bot.send_message(message.chat.id, greeting, reply_markup=markup, parse_mode='html')
    await btn_classes.stick.send_stickers(bot, message)


@bot.callback_query_handler(func=lambda callback: callback.message.chat.type == 'private')
async def set_notifications(callback):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    await btn_classes.db_conn.db_set_time(bot, callback.message, callback.data)


@bot.callback_query_handler(func=lambda callback: callback.message.chat.type == 'supergroup')
async def confirm_callback(callback):
    if callback.data == 'Подтвердить':
        user_message = callback.message.text.split('\n')
        user_id = int(user_message[1].split(':')[-1][1:])
        user_name = user_message[2].split(':')[-1][1:] if user_message[2].split(':')[-1][1:] != 'None' else None
        user_surname = user_message[3].split(':')[-1][1:] if user_message[3].split(':')[-1][1:] != 'None' else None
        username = user_message[4].split(':')[-1][1:] if user_message[4].split(':')[-1][1:] != 'None' else None
        user_msg = ''.join(user_message[5:-1])[''.join(user_message[5:-1]).index('Задание: ') + len('Задание: '):]
        await btn_classes.db_conn.db_write_task(bot, callback.message, user_id, user_name, user_surname, username,
                                                user_msg)
        markup = types.InlineKeyboardMarkup()
        text = '\n'.join(callback.message.text.split('\n')[:-1]) + '\n<strong>Статус:</strong> Одобрено ' + u'\u2705'
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup, parse_mode='html')

    elif callback.data == 'Не подтвердить':
        markup = types.InlineKeyboardMarkup(row_width=1)
        text = '\n'.join(callback.message.text.split('\n')[:-1]) + '\n<strong>Статус:</strong> Отказано '\
               + u'\u274C' + '\n<strong>Причина: </strong>'
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markup, parse_mode='html')


@bot.message_handler(content_types=['text'], chat_types=['supergroup'])
async def reply_msg(reply):
    if reply.reply_to_message is not None and u'\u274C' in reply.reply_to_message.text.split('\n')[-2]:
        reason = '\n'.join(reply.reply_to_message.text.split('\n')[:-2])\
                 + f'\n<strong>Статус:</strong> Отказано ' + u'\u274C'\
                 + f'\n<strong>Причина:</strong> {reply.text}'
        await bot.edit_message_text(chat_id=reply.chat.id, message_id=reply.reply_to_message.id, text=reason,
                                    parse_mode='html')
        markup = btn_classes.init_btns()
        user_id = int(reply.reply_to_message.text.split('\n')[1].split(':')[-1][1:])
        text = f'Ваше сообщение не было одобрено, модератор высказал причину:\n\n{reply.text}\n\n'
        task = '\n'.join(reply.reply_to_message.text.split('\n')[-3:-2])['\n'.join(reply.reply_to_message.text.split('\n')[-3:-2]).index('Задание: ') + len('Задание: '):]
        task = '<strong>Задание:\n</strong>' + task
        await bot.send_message(user_id, text + task, reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=[comm[1:] for comm in useful_msg], chat_types=['private'])
async def basic_commands(message):
    btn_classes.notifies.flag_location[message.chat.id] = False
    btn_classes.stick.flag[message.from_user.id] = None
    for msg in useful_msg:
        if message.text.lower() == msg:
            await useful_msg[msg](bot, message)
            break


@bot.message_handler(content_types=['location', 'venue'], chat_types=['private'])
async def geo_location(message):
    btn_classes.stick.flag[message.from_user.id] = None
    if message.location is not None and btn_classes.notifies.flag_location[message.chat.id]:
        await btn_classes.db_conn.db_update_task(bot, message)


@bot.message_handler(content_types=['text'], chat_types=['private'])
async def get_private_message(message):
    btn_classes.stick.flag[message.chat.id] = None
    btn_classes.notifies.flag_location[message.chat.id] = False
    if btn_classes.stick.stick_sending.get(message.chat.id):
        markup = types.ReplyKeyboardMarkup()
        markup.add('/stop_stickers')
        await bot.send_message(message.chat.id, 'Закончите отправку стикеров (кнопка "stop_stickers")',
                               reply_markup=markup)
    elif btn_classes.db_conn.stack_write_db_task.get(message.chat.id):
        btn_classes.db_conn.msgs[message.chat.id] = message
        btn_classes.db_conn.stack_write_db_task[message.chat.id] = False
        await btn_classes.db_conn.db_before_confirm_task(bot, message)

    else:
        markup = btn_classes.init_btns()
        await bot.send_message(message.chat.id, 'Я так не понимаю :(\nВыбери какую-то команду!',
                               reply_markup=markup)


@bot.message_handler(content_types=['sticker'], chat_types=['private'])
async def get_sticker_messages(sticker):
    btn_classes.stick.flag_location[sticker.from_user.id] = False
    data = btn_classes.open_file('data_stick.json')
    if btn_classes.stick.flag[sticker.from_user.id] is not None and btn_classes.stick.flag[sticker.from_user.id]:
        if data.get(str(sticker.from_user.id)):
            data[str(sticker.from_user.id)].update({sticker.sticker.file_unique_id: sticker.sticker.file_id})
        else:
            data[str(sticker.from_user.id)] = {sticker.sticker.file_unique_id: sticker.sticker.file_id}
    elif (btn_classes.stick.flag[sticker.from_user.id] is not None
          and not btn_classes.stick.flag[sticker.from_user.id]
          and sticker.sticker.file_unique_id in data[str(sticker.from_user.id)]):
        del data[str(sticker.from_user.id)][sticker.sticker.file_unique_id]
    if not data[str(sticker.from_user.id)]:
        del data[str(sticker.from_user.id)]
    with open('data_stick.json', 'w') as file:
        json.dump(data, file, indent=4)


async def main():
    await asyncio.gather(bot.polling(interval=1,
                                     non_stop=True,
                                     timeout=1000,
                                     request_timeout=1000),
                         timer.try_send_schedule(),
                         timer.update_sch()
                         )

if __name__ == '__main__':
    asyncio.run(main())
