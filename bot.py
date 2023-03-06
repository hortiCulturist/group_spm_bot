import time

from pyrogram.enums import ChatType

import config
from pyrogram import Client, filters
from pyrogram.types import Message
import db
from datetime import timedelta, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler


config.trigger = False


async def update_last_time_send(task_id, interval):
    minutes = str(interval).split(':')[1]
    send_time = round(time.time()) + int(minutes) * 60
    db.add_send_time(send_time, task_id)


async def send_all_messages():
    for data in db.get_my_channel():
        if config.trigger:
            if round(time.time()) > data[5]:
                try:
                    await bot.copy_message(chat_id=data[1],
                                           from_chat_id=data[3],
                                           message_id=data[2])
                    await update_last_time_send(data[0], data[4])
                except Exception as e:
                    print(f'Ошибка отправки\n\n'
                          f'{e}')


scheduler = AsyncIOScheduler()


db.start_db()
scheduler.start()
scheduler.add_job(send_all_messages, "interval", seconds=5)
bot = Client("my_account",
             api_id=config.api_id,
             api_hash=config.api_hash)
print("Bot started")


# add new pattern *group_id* *message_id* *message_chat_id* *time_interval* *next_send*
@bot.on_message(filters.regex('^add new pattern'))
async def new_pattern(_, message: Message):
    text = message.text
    text = text.split()
    db.add_pattern(text)
    await bot.send_message(message.from_user.id, 'Паттерн добавлен')


# delete *id*
@bot.on_message(filters.regex('^delete'))
async def new_pattern(_, message: Message):
    text = message.text.split()
    db.delete(text[1])
    await bot.send_message(message.from_user.id, text='Паттерн удалён')


# view all pattern
@bot.on_message(filters.regex('^view all pattern'))
async def new_pattern(_, message: Message):
    for i in db.view_all_pattern():
        await bot.send_message(message.from_user.id, f'ID паттерна: {i[0]}\n'
                                                     f'ID группы: {i[1]}\n'
                                                     f'Интервал: {i[2]}\n')


@bot.on_message(filters.regex('^help$'))
async def chat_list_downloader(_, message: Message):
    await bot.send_message(message.from_user.id, f'**Добавить паттерн:**\n'
                                                 f'add new pattern (group_id) '
                                                 f'(0) '
                                                 f'(0) '
                                                 f'(time_interval)'
                                                 f'(0)\n'
                                                 f'Пример: add new pattern -123456789 0 0 0:04 0'
                                                 f'\n\n'

                                                 f'**Посмотреть все паттерны:**\n'
                                                 f'view all pattern\n\n'

                                                 f'**Запуск рассылки:**\n'
                                                 f'start\n\n'

                                                 f'**Остановка рассылки:**\n'
                                                 f'stop\n\n'

                                                 f'**Посмотреть ID всех групп аккаунта**\n'
                                                 f'get\n\n'

                                                 f'**Удалить паттерн:**\n'
                                                 f'delete (ID паттерна)\n'
                                                 f'Пример: delete 3\n\n'

                                                 f'<**Важно соблюдать регистр команд и пробелы**>\n')


@bot.on_message(filters.regex('^get'))
async def get_groups(_, message: Message):
    message_text = 'Список групп аккаунта:'
    all_dialog = bot.get_dialogs()
    async for dialog in all_dialog:
        if dialog:
            if dialog.chat.type == ChatType.GROUP or ChatType.SUPERGROUP:
                message_text += f"\nname: {dialog.chat.title}\n"
                message_text += f"group id: {dialog.chat.id}\n"
    await bot.send_message(message.from_user.id, message_text)


@bot.on_message(filters.regex('^start'))
async def get_groups(_, message: Message):
    config.trigger = True
    await bot.send_message(message.from_user.id, text='Отправка запущена')


@bot.on_message(filters.regex('^stop'))
async def get_groups(_, message: Message):
    config.trigger = False
    await bot.send_message(message.from_user.id, text='Отправка остановлена')


# @bot.on_message(filters.regex('^send'))
# async def start_posting(_, message: Message):
#     for data in db.get_my_channel():
#         min = str(data[4]).split(':')
#         print(min)
#         time_now = datetime.now()
#         send_time = round(datetime.timestamp(time_now + timedelta(minutes=float(min[1]))))
#         db.add_send_time(send_time, data[0])


@bot.on_message(filters.chat(config.admin_id))
async def create_new_post(_, message: Message):
    for data in db.get_my_channel():
        db.update_message(data[0])
    db.add_message_db(message.id, message.chat.id)
    await bot.send_message(message.from_user.id, text='Пост добавлен')


if __name__ == '__main__':
    bot.run()