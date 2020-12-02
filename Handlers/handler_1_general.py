from aiogram import types
from misc import dp
from config import ADMIN_ID


@dp.message_handler(chat_type='private', commands=['commands', 'list', 'help'])
@dp.message_handler(user_id=ADMIN_ID, commands=['commands', 'list', 'help'])
async def commands_list(message: types.Message):
    """Список всех команд"""
    text = \
        'Список команд:\n\n' + \
        '/about_cod_bot - о боте,\n' + \
        '/commands - список основных команд,\n' + \
        '/add_me - добавить свой профиль (работает только при отправке запроса в личные сообщения БОТу),\n' + \
        '/edit_me - редактировать свой профиль (работает только при отправке запроса в личные сообщения БОТу),\n' + \
        '/stat - показывает информацию о КД всех упомянутых в сообщении людей (при их отсутствии показывает Ваш КД),\n' + \
        '/stat_update - обновить информацию о своём КД (работает только при отправке запроса в личные сообщения БОТу).\n' + \
        '/show_full_profile_info - показать ПОЛНУЮ информацию о профиле (работает только при отправке запроса в личные сообщения БОТу).'
    if message.from_user.id == ADMIN_ID:
        text += '\n\nСписок команд для администраторов:\n\n' + \
                '/set_commands - установить команды вместо BotFather,\n' + \
                '/clear_commands - удалить команды вместо BotFather,\n' +  \
                '/chat_info - вывести ID чата,\n' + \
                '/stats_update_all - обновляет статистику по КД всем зарегистрированным пользователей.\n' + \
                '/add_all_psn_to_friends - добавить всех в друзья по psn,\n' + \
                '/stats_all - показать информацию о всех пользователях и их КД'
    await message.answer(text=text, reply=False)
