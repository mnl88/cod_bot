"""
Хэндлеры, обращающиеся к БД, только с правами чтения
"""

from misc import dp
from alchemy import get_member, get_all_members
from aiogram import types
from .handler_0_middleware import load_profile, load_kd


@dp.message_handler(commands=['show_profile'])
async def show_profile(message: types.Message, is_reply=True):
    """показывает данные пользователя"""
    await types.ChatActions.typing()
    if not get_member(message.from_user.id):
        await message.answer(
            'Для отображения статистики необходимо сообщить мне свой ACTIVISION ID: /add_me', reply=True)
    else:
        cod_user = get_member(message.from_user.id)
        text = load_profile(cod_user)
        await message.answer(text, reply=is_reply)


@dp.message_handler(commands=['show_my_stats', 'show_me', 'me'])
async def show_stats(message: types.Message):
    """показывает статистику игрока"""
    await types.ChatActions.typing()
    if not get_member(message.from_user.id):
        await message.answer(
            'Для отображения статистики необходимо сообщить мне свой ACTIVISION ID: /add_me', reply=True)
    else:
        cod_user = get_member(message.from_user.id)
        text = load_profile(cod_user) + load_kd(cod_user)
        await message.answer(text, reply=True)


@dp.message_handler(commands="show_players_stats")
async def show_players_stats(message: types.Message, is_reply=True):
    """показывает статистику всех игроков в базе данных"""
    await types.ChatActions.typing()
    players = get_all_members()
    text = ''
    for player in players:
        if player.activision_id != 'Unknown'.lower():
            if player.tg_name != 'unknown':
                text += "Имя в Телеге: @" + str(player.tg_name) + "\n"
            text2 = "ACTIVISION ID: " + str(player.activision_id) + "\n"
            text3 = "К/Д в Варзоне: " + str(player.kd_warzone) + "\n"
            text4 = "К/Д в мультиплеере: " + str(player.kd_multiplayer) + "\n\n"
            text += text2 + text3 + text4
    await message.answer(text, reply=is_reply)
