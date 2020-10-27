from aiogram import types
from misc import dp, bot
from config import ADMIN_ID

user_commands_list = ''
admin_commands_list = '/set_commands - УСТАНОВИТЬ КОМАНДЫ вместо BotFather\n'


@dp.message_handler(user_id=ADMIN_ID, commands="set_commands")
async def set_commands_to_bf(message: types.Message):
    """УСТАНОВИТЬ КОМАНДЫ вместо BotFather"""

    commands = [types.BotCommand(command="/about", description="О боте"),
                types.BotCommand(command="/command_list", description="Список основных команд"),
                types.BotCommand(command="/me", description="Показать информацию о своём профиле"),
                types.BotCommand(command="/edit_me", description="Редактировать свой профиль"),
                types.BotCommand(command="/stat", description="Показать информацию о своём КД"),
                types.BotCommand(command="/stat_update", description="Обновить информацию о своём КД")]
    await bot.set_my_commands(commands)
    await message.answer("Команды настроены. Перезапустите Telegram")


@dp.message_handler(user_id=ADMIN_ID, commands="clear_commands")
async def set_commands_to_bf(message: types.Message):
    """удалить КОМАНДЫ вместо BotFather"""
    await bot.set_my_commands([])
    await message.answer("Команды очищены. Перезапустите Telegram")


@dp.message_handler(user_id=ADMIN_ID, commands="chat_info")
async def chat_info(message: types.Message):
    """вывести в Телеграм ID чата"""

    text = f"Заголовок: {str(message.chat.title)}\nID этого чата: {str(message.chat.id)}"
    await message.answer(text=text, reply=False)
