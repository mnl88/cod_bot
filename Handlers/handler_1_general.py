from aiogram import types
from misc import dp
from config import ADMIN_ID



@dp.message_handler(commands=['about', 'start'])
async def about_bot(message: types.Message):
    """Информация о боте"""
    await message.reply(
        text='''Данный бот написан для предоставления пользователям информации по своей статистике в игре ''' +
             '''CALL OF DUTY и упрощения коммуникации участников тематической группы ''' +
             '''https://t.me/ruszone.\n''' +
             '''Для полноценной работы необходимо внести данные своей учётной записи с помощью команды: /add_me\n''' +
             '''Справка по основным командам: /help\n\n''' + '''автор: @MaNiLe88''',
             reply=True)


@dp.message_handler(commands=['command_list', 'list'])
async def commands_list(message: types.Message):
    """Список всех команд"""
    text = 'Список команд:\n' + 'empty'
    if message.from_user.id == ADMIN_ID:
        text += '\n\nСписок команд для администраторов:\n' + 'empty'
    await message.answer(text=text, reply=False)
