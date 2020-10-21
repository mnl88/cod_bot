from aiogram import types
from misc import dp, bot
import config


user_commands_list = ''
admin_commands_list = '/set_commands - УСТАНОВИТЬ КОМАНДЫ вместо BotFather\n'

# УСТАНОВИТЬ КОМАНДЫ вместо BotFather
@dp.message_handler(user_id=config.ADMIN_ID, commands="set_commands")
async def set_commands_to_bf(message: types.Message):
    commands = [types.BotCommand(command="/about", description="О боте"),
                types.BotCommand(command="/help", description="Список основных команд"),
                types.BotCommand(command="/me", description="Показать информацию о своём КД"),
                types.BotCommand(command="/update_me", description="Обновить информацию о своём КД")]
    await bot.set_my_commands(commands)
    await message.answer("Команды настроены. Перезапустите Telegram")


