import logging

import fastapi as fastapi
from aiogram import types, Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import telebot


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






'''app = fastapi.FastAPI(docs=None, redoc_url=None)
bot = telebot.TeleBot(TOKEN)

@app.post(f'/{TOKEN}/')
def process_webhook(update: dict):

    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return

@dp.message_handler(lambda message: True, content_types=['text'])
async def echo_message (message):

     await message.reply(message.text)


executor.start_polling(dp, skip_updates=True, on_startup=one_startup)'''








