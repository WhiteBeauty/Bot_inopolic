import logging
from aiogram import types, Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3 as sq
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.executor import start_webhook

from settins import TOKEN


storage=MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

async def one_startup(_):
    print('Бот вышел в онлайн')



'''WEBHOOK_HOST = 'https://63d2-95-153-179-202.eu.ngrok.io'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 8000

logging.basicConfig(level=logging.INFO)'''


class FSMAdmin(StatesGroup):
    photo = State()



def sql_start():
    global base, cur
    base = sq.connect('advertisement.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()



async def sql_add_command(state):
    async with state.proxy() as date:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(date.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0])

async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()





@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')




@dp.message_handler(content_types = ['photo'])
async def echo_photo_bot(message):
    await bot.send_photo(message.from_user.id, photo=message.photo[0].file_id, caption=message.caption)








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

executor.start_polling(dp, skip_updates=True, on_startup=one_startup)

'''async def on_startup(dp):
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
'''




'''if __name__ == '__main__':
   start_webhook(
       dispatcher=dp,
       webhook_path=WEBHOOK_PATH,
       on_startup=on_startup,
       on_shutdown=on_shutdown,
       skip_updates=True,
       host=WEBAPP_HOST,
       port=WEBAPP_PORT,
   )'''



# my github: https://github.com/WhiteBeauty/Bot_inopolic











