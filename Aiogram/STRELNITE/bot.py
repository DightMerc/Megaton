import asyncio
import logging

from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor


API_TOKEN = '679147382:AAGRMZ1t2wrGuYBQOMg-jhNiWnWNUUOkDUM'

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("What cam you say About PyCharm???")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, caption='Cats is here 😺',
                             reply_to_message_id=message.message_id)


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)

    ##Can you hear me?