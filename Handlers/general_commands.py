from aiogram import types
from misc import dp, bot
import config

user_commands_list = '/about, /start - start,\n'
admin_commands_list = ''


# Команда О БОТЕ
@dp.message_handler(commands=['about', 'start'])
async def send_menu(message: types.Message):
    """отправить список команд бота"""
    await message.reply(text=
                        '''Данный бот написан для упрощения коммуникации участников группы''' +
                        ''' https://t.me/ruszone\n\nСправка по основным командам /help\n\n''' + '''автор: @MaNiLe88''',
                        reply=True)




