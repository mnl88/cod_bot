from aiogram import types
from misc import dp, bot
import config

user_id_required = config.ADMIN_ID


# Список команд для админимтраторов
@dp.message_handler(user_id=user_id_required, commands=['admin_help'])
async def admin_help(message: types.Message):
    await message.answer("""Уже скоро здесь будет список всех команд, доступных только для админов!!!!
    \n\n
    /set_commands - УСТАНОВИТЬ КОМАНДЫ вместо BotFather\n
    /chat_id - Узнать ID чата
    """)


# УСТАНОВИТЬ КОМАНДЫ вместо BotFather
@dp.message_handler(user_id=user_id_required, commands="set_commands")
async def cmd_set_commands(message: types.Message):
    commands = [types.BotCommand(command="/about", description="О боте"),
                types.BotCommand(command="/help", description="Список основных команд"),
                types.BotCommand(command="/me", description="Показать информацию о своём КД"),
                types.BotCommand(command="/update_me", description="Обновить информацию о своём КД")]
    await bot.set_my_commands(commands)
    await message.answer("Команды настроены. Перезапустите Telegram")


