from aiogram import types
from misc import dp, bot
import config

from . import admin_handler
from . import cod_statistics
from . import general_commands
from . import keyboard_training
from . import new_handler
from . import practic
from . import schedule_commands
from . import schedule_commandsAAA

user_commands_list = admin_handler.user_commands_list + \
                     cod_statistics.user_commands_list + \
                     general_commands.user_commands_list + \
                     keyboard_training.user_commands_list + \
                     new_handler.user_commands_list + \
                     practic.user_commands_list + \
                     schedule_commands.user_commands_list + \
                     schedule_commandsAAA.user_commands_list

admin_commands_list = admin_handler.admin_commands_list + \
                      cod_statistics.admin_commands_list + \
                      general_commands.admin_commands_list + \
                      keyboard_training.admin_commands_list + \
                      new_handler.admin_commands_list + \
                      practic.admin_commands_list + \
                      schedule_commands.admin_commands_list + \
                      schedule_commandsAAA.admin_commands_list


# Список всех команд
@dp.message_handler(commands=['list'])
async def commands_list(message: types.Message):
    text = 'Список команд:\n\n' + user_commands_list
    if message.from_user.id == config.ADMIN_ID:
        text += '\n\nСписок команд для администраторов:\n\n' + admin_commands_list
    await message.answer(text=text, reply=False)
