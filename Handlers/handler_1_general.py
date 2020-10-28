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


@dp.message_handler(commands=['command_list', 'list', 'help'])
async def commands_list(message: types.Message):
    """Список всех команд"""
    text = \
        'Список команд:\n\n' + \
        '/about - о боте,\n' + \
        '/command_list - список основных команд,\n' + \
        '/me - показать информацию о своём профиле,\n' + \
        '/edit_me - редактировать свой профиль (работает только при отправке запроса в личные сообщения БОТу),\n' + \
        '/stat - показать информацию о своём КД,\n' + \
        '/stat_update - обновить информацию о своём КД (работает только при отправке запроса в личные сообщения БОТу).'
    if message.from_user.id == ADMIN_ID:
        text += '\n\nСписок команд для администраторов:\n\n' + \
                '/set_commands - установить команды вместо BotFather,\n' + \
                '/clear_commands - удалить команды вместо BotFather,\n' +  \
                '/chat_info - вывести ID чата,\n' + \
                '/stats_update_all - обновляет статистику по КД всем зарегистрированным пользователей.\n' + \
                '/stats_all - показать информацию о всех пользователях и их КД'
    await message.answer(text=text, reply=False)
