import asyncio
from datetime import *
from misc import dp
from aiogram import *

user_commands_list = ''
admin_commands_list = '/spam - spam'


@dp.message_handler(commands="spam")
async def status_set(message: types.Message):
    while True:
        await asyncio.sleep(4)
        print(datetime.now())


# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)

