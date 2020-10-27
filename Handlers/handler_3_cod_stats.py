"""
Хэндлеры, обращающиеся к БД, только с правами чтения
"""

from .handler_0_middleware import load_profile, load_kd
from misc import dp
from alchemy import session
from alchemy import get_member, get_all_members, datetime, COD_User
from aiogram import types
from cod_stats_parser import parser_act_id
from config import ADMIN_ID


# Показывает данные пользователя (Имя, Activision ID и PSN ID)
@dp.message_handler(commands=['profile', 'me'])
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


# Показывает статистику по КД
@dp.message_handler(commands=['stat'])
async def show_stat(message: types.Message):
    """показывает статистику игрока"""
    await types.ChatActions.typing()
    if not get_member(message.from_user.id):
        await message.answer(
            'Для отображения статистики необходимо сообщить мне свой ACTIVISION ID: /add_me', reply=True)
    else:
        cod_user = get_member(message.from_user.id)
        text = load_profile(cod_user) + load_kd(cod_user)
        await message.answer(text, reply=True)


# Показывает статистику по КД всех зарегистрированных пользователей
@dp.message_handler(commands="stats_all")
async def show_stats_all(message: types.Message, is_reply=True):
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


# Обновляет статистику по КД
@dp.message_handler(commands=['stat_update'])
async def stat_update(message: types.Message):
    member = get_member(message.from_user.id)
    print(member)
    await types.ChatActions.typing()
    if member.activision_id != 'Unknown'.lower():
        member.kd_warzone = parser_act_id(member.activision_id, 'WZ')
        member.kd_multiplayer = parser_act_id(member.activision_id, 'MP')
        member.update_kd = datetime.now()
        member.tg_name = message.from_user.username
        session.add(member)
        session.commit()
        print(member)
        print(member.kd_warzone)
        print(member.kd_multiplayer)
        await message.answer(message.from_user.first_name + ", статистика обновлена")
    else:
        await message.answer(message.from_user.first_name +
                             ", вам необходимо уточнить свой ACTIVISION_ID, для этого воспользуйтесь командой /add_me")


# Обновляет статистику по КД всем зарегистрированным пользователей
@dp.message_handler(user_id=ADMIN_ID, commands=['stats_update_all'])
async def stats_update_all(message: types.Message):
    players = get_all_members()
    for player in players:
        await types.ChatActions.typing()
        player.kd_warzone = parser_act_id(player.activision_id, 'WZ')
        player.kd_multiplayer = parser_act_id(player.activision_id, 'MP')
        player.update_kd = datetime.now()
        print(player)
        print(player.kd_warzone)
        print(player.kd_multiplayer)
        session.add(player)
    session.commit()
    await message.answer(message.from_user.first_name + ", статистика обновлена")
