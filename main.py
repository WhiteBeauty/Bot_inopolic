import logging
from aiogram import types, Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3 as sq

from aiogram.utils.executor import start_webhook

from settins import TOKEN


storage=MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

async def one_startup(_):
    print('Бот вышел в онлайн')



WEBHOOK_HOST = 'https://63d2-95-153-179-202.eu.ngrok.io'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 8000

logging.basicConfig(level=logging.INFO)


@dp.message_handler(text='база')
async def user_db(message: types.Message):
    con = sq.connect('users.db')
    cur = con.cursor()
    user = cur.execute('SELECT * FROM users')
    user = user.fetchall()
    if user:
        print("YES")
    else:
        print("error, you are not user")

def create_table():
    con = sq.connect('users.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
             userid INT PRIMARY KEY,
             username TEXT)
         """)
    con.commit()
    cur.close()
    con.close()


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет, рад знакомству! Чем я могу тебе помочь?')
    await message.delete()

@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Это телеграм бот, он умеет повторять')


@dp.message_handler(commands=['copy'])
async def send_copy(message: types.Message):
    await message.reply("Копия сообщения: " + message.text[6:])


@dp.message_handler(content_types=['text'])
async def get_text_messages(message):
    if message.text == "/help":
        await bot.send_message(message.from_user.id, "Напиши /start")
    else:
        await message.reply(message.text)
        await bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")



async def on_startup(dp):
   await bot.set_webhook(WEBHOOK_URL)
   # insert code here to run it after start


async def on_shutdown(dp):
   logging.warning('Shutting down..')

   # insert code here to run it before shutdown

   # Remove webhook (not acceptable in some cases)
   await bot.delete_webhook()

   # Close DB connection (if used)
   await dp.storage.close()
   await dp.storage.wait_closed()

   logging.warning('Bye!')





if __name__ == '__main__':
   start_webhook(
       dispatcher=dp,
       webhook_path=WEBHOOK_PATH,
       on_startup=on_startup,
       on_shutdown=on_shutdown,
       skip_updates=True,
       host=WEBAPP_HOST,
       port=WEBAPP_PORT,
   )



# my github: https://github.com/WhiteBeauty/Bot_inopolic











