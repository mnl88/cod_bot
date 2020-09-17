import config
from aiogram import types
from misc import dp
from alchemy import *
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from cod_stats_parser import *
import asyncio

session = db_init()


@dp.message_handler(user_id=config.ADMIN_ID, commands="chat_info")
async def chat_info(message: types.Message):
    print(f"Заголовок: {str(message.chat.title)}\nID этого чата: {str(message.chat.id)}")


@dp.message_handler(user_id=config.ADMIN_ID, commands="add_manile")
async def add_me_for_test(message: types.Message):
    tg_id = 202181776
    manile = get_member(session, tg_id)
    if manile is False:
        print('нету Manile')
        manile = COD_User(tg_id=tg_id)
        manile.tg_name = 'MaNiLe88'
        manile.name = 'Никита'
        manile.activision_id = 'Imago#1393409'
        session.add(manile)
        session.commit()
        await message.answer("выполнено")
    print(type(manile))


# Обновление всем статистики
@dp.message_handler(commands=['update_all'])
async def update_all(message: types.Message):
    players = get_all_members(session)
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


# Обновление своей статистики
@dp.message_handler(commands=['update_me'])
async def update_me(message: types.Message):
    me = get_member(session, message.from_user.id)
    print(me)
    await types.ChatActions.typing()
    if me.activision_id != 'Unknown'.lower():
        me.kd_warzone = parser_act_id(me.activision_id, 'WZ')
        me.kd_multiplayer = parser_act_id(me.activision_id, 'MP')
        me.update_kd = datetime.now()
        me.tg_name = message.from_user.username
        session.add(me)
        session.commit()
        print(me)
        print(me.kd_warzone)
        print(me.kd_multiplayer)
        await message.answer(message.from_user.first_name + ", статистика обновлена")
    else:
        await message.answer(message.from_user.first_name +
                             ", вам необходимо уточнить свой ACTIVISION_ID, для этого воспользуйтесь командой /add_me")


@dp.message_handler(commands="show_players_stats")
async def show_players_stats(message: types.Message):
    """показывает статистику всех игроков в базе данных"""
    await types.ChatActions.typing()
    players = get_all_members(session)
    text = ''
    for player in players:
        if player.activision_id != 'Unknown'.lower():
            if player.tg_name != 'unknown':
                text += "Имя в Телеге: @" + str(player.tg_name) + "\n"
            text2 = "ACTIVISION ID: " + str(player.activision_id) + "\n"
            text3 = "К/Д в Варзоне: " + str(player.kd_warzone) + "\n"
            text4 = "К/Д в мультиплеере: " + str(player.kd_multiplayer) + "\n\n"
            text += text2 + text3 + text4
    await message.answer(text, reply=True)


@dp.message_handler(commands=['show_my_stats', 'show_me', 'me'])
async def show_my_stats(message: types.Message):
    """показывает статистику игрока"""
    await types.ChatActions.typing()
    if not get_member(session, message.from_user.id):
        await message.answer('Для отображения статистики необходимо указать свой ACTIVISION ID /add_me', reply=True)
    else:
        me = get_member(session, message.from_user.id)
        text = ''
        text0 = "Имя/ник: " + str(me.name) + "\n"
        if me.tg_name != 'unknown':
            text0 += "Имя в Телеге: @" + str(me.tg_name) + "\n"
        text11 = "ACTIVISION ID: " + str(me.activision_id) + "\n"
        text2 = "PSN ID: " + str(me.psn_id) + "\n"
        text3 = "К/Д в Варзоне: " + str(me.kd_warzone) + "\n"
        text4 = "К/Д в мультиплеере: " + str(me.kd_multiplayer) + "\n\n"
        text5 = "Last update: " \
                + "\n" + str(me.update_kd.strftime("%d.%m.%Y")) \
                + "\n" + str(me.update_kd.strftime("%H:%M:%S"))
        text += text0 + text11 + text2 + text3 + text4 + text5
        await message.answer(text, reply=True)
