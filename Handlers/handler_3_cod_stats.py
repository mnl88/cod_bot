"""
Хэндлеры, обращающиеся к БД, только с правами чтения
"""

from .handler_0_middleware import load_profile, load_kd
from misc import dp
from alchemy import session
from alchemy import get_member, get_all_members, datetime, COD_User
from aiogram import types
from cod_stats_parser import parser_act_id
from config import ADMIN_ID, COD_CHAT_ID
import re
import logging


logger = logging.getLogger(__name__)


# Показывает данные пользователя (Имя, Activision ID и PSN ID)
@dp.message_handler(chat_type='private', commands=['profile'])
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

    members = []

    pattern = re.compile('@+\w{0,100}')  # паттерн, для нахождения упоминаний в тексте
    username_list = re.findall(pattern, message.text)  # Список упоминаний по username в данном сообщении
    print(f'В указанном тексте {len(username_list)} упоминаний по username')

    # часть кода, для mention
    for mention in username_list:
        mention = mention.replace('@', '')  # Удалим из списка символ @
        print(f'Username = {mention}')
        await types.ChatActions.typing()  # бот типа печатает
        member = get_member(tg_name=mention)
        if member is not False:
            print(f'{member=}')
            members.append(member)

    # часть кода, для text_mention
    for entity in message.entities:  # перебираем сущности
        if entity.type == 'text_mention':  # если находим упоминания
            await types.ChatActions.typing()  # бот типа печатает
            member = get_member(tg_id=entity.user.id)
            if member is not False:
                print(f'{member=}')
                members.append(member)

    # если упоминаний нет, то добавляем в список себя
    if len(members) == 0:

        if get_member(message.from_user.id):
            me = get_member(message.from_user.id)
            members.append(me)
        else:
            await message.answer(
                'Для отображения статистики необходимо сообщить мне свой ACTIVISION ID, для этого напишите личное сообщение боту напрямую', reply=True)

    await show_statistic(message, members)


# Показывает статистику по КД
async def show_statistic(message: types.Message, members: list):
    """показывает статистику игрока"""
    if len(members) != 0:
        for member in members:
            await types.ChatActions.typing()
            text = load_profile(member) + load_kd(member)
            await message.answer(text, reply=True)


# Показывает статистику по КД всех зарегистрированных пользователей
@dp.message_handler(chat_type=['group', 'supergroup'], is_chat_admin=True,
                    chat_id=COD_CHAT_ID, commands=['stats_all'])
@dp.message_handler(user_id=ADMIN_ID, commands=['stats_all'])
async def show_stats_all(message: types.Message, is_reply=True):
    """показывает статистику всех игроков в базе данных"""
    logger.info(
        f'Хэндлер STATS_ALL запущен пользователем с id {message.from_user.id} '
        f'({message.from_user.full_name}, {message.from_user.username})')
    await types.ChatActions.typing()
    players = get_all_members()
    logger.info(f'Из БД загружено {len(players)} записей')
    text = ''
    players_with_kd = []
    for player in players:  # Обрезаем тех, чье КД = None
        a = player.kd_warzone
        if a != 'unknown':
            print(player, a)
            players_with_kd.append(player)

    for player in sorted(players_with_kd, key=lambda user: user.kd_warzone, reverse=True):
        if player.tg_name != 'unknown':
            text += "Имя в Телеге: @" + str(player.tg_name) + "\n"
        text2 = "ACTIVISION ID: " + str(player.activision_id) + "\n"
        text3 = "К/Д в Варзоне: " + str(player.kd_warzone) + "\n"
        text4 = "К/Д в мультиплеере: " + str(player.kd_multiplayer) + "\n\n"
        text += text2 + text3 + text4
    await message.answer(text, reply=is_reply)


# Обновляет статистику по КД
@dp.message_handler(chat_type='private', commands=['stat_update'])
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
@dp.message_handler(chat_type=['group', 'supergroup'], is_chat_admin=True,
                    chat_id=COD_CHAT_ID, commands=['stats_update_all'])
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


@dp.message_handler(chat_type=['group', 'supergroup', 'private'], commands=['stats_update_all', 'stats_all'])
async def show_stats_all(message: types.Message, is_reply=True):
    """показывает статистику всех игроков в базе данных"""
    await types.ChatActions.typing()
    await message.answer(
        'Данную команду может выполнить только пользователь с правами админимтратора', reply=is_reply)
