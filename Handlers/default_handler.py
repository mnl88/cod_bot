from aiogram import types
from misc import dp
import config


@dp.message_handler(user_id=config.manile_id, content_types=types.ContentTypes.ANY)
async def all_other_messages(message: types.Message):
    await message.reply("Серёжка Фастовец - дурачок!", reply=True)
    # print(message.from_user.id)


@dp.message_handler(user_id=config.Fastovets, content_types=types.ContentTypes.ANY)
async def admin_help(message: types.Message):
    await message.reply(message.from_user.first_name + """- ты дурачок
    """, reply=True)