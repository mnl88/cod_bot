from aiogram import types
from misc import dp, bot
import config


# Команда О БОТЕ
@dp.message_handler(commands=['about', 'start'])
async def send_menu(message: types.Message):
    """отправить список команд бота"""
    await message.reply(text=
                        '''Данный бот написан для упрощения коммуникации участников группы''' +
                        ''' https://t.me/ruszone\n\nСправка по основным командам /help\n\n''' + '''автор: @MaNiLe88''',
                        reply=True)


# Команда ХЕЛП
@dp.message_handler(commands=['list', 'help', 'info'])
async def send_menu(message: types.Message):
    """отправить список команд бота"""
    if message.from_user.id == config.ADMIN_ID:
        await message.reply(text=
                            '''/about  - О боте,\n''' +
                            '''/add_me - добавить меня в базу данных,\n''' +
                            '''/delete_me - удалить меня из базы данных,\n''' +
                            '''/update_me - Обновить информацию о своём КД,\n''' +
                            '''/me - показать информацию о своём КД,\n''' +
                            '''/set_commands - Только для админов.\n''',
                            reply=True)
    else:
        await message.reply(text=
                            '''/about  - О боте,\n''' +
                            '''/add_me - добавить меня в базу данных,\n''' +
                            '''/delete_me - удалить меня из базы данных (НЕ РЕАЛИЗОВАНО),\n''' +
                            '''/update_me - Обновить информацию о своём КД,\n''' +
                            '''/me - показать информацию о своём КД,\n''',
                            reply=True)


@dp.message_handler(user_id=config.ADMIN_ID, commands=['list2', 'help2', 'info2'])
async def chat_info(message: types.Message):
    await message.answer(
        "add_manile: /add_manile" + "\n" +
        "chat_info: /chat_info" + "\n" +
        "start: /start" + "\n" +
        "add_me: /add_me" + "\n" +
        "update_all: /update_all" + "\n" +
        "show_players_stats: /show_players_stats"
    )



