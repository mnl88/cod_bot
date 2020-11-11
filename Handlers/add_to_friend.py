from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from re import compile
from misc import dp
from config import ADMIN_ID, COD_CHAT_ID, PSN_EMAIL, PSN_PASSWORD, PSN_USERNAME
from alchemy import get_all_members, COD_User
from psn_selenium_parser import PSN_Bot
import asyncio
import random


# Запускаем бот из группы
@dp.message_handler(user_id=ADMIN_ID, chat_type='private', commands=['add_all_psn_to_friends'])
async def add_all_psn_to_friends(message: types.Message):

    members = get_all_members()
    members_with_psn = []
    print(f'Всего профилей в БД: {len(members)}\n')
    for user in members:
        user: COD_User
        if user.psn_id != 'unknown':
            print(f'{user} - PSN указан ({user.psn_id})')
            members_with_psn.append(user)

    print(f'Всего профилей в БД c PSN: {len(members_with_psn)}\n')

    ps_pars = PSN_Bot(PSN_USERNAME, PSN_EMAIL, PSN_PASSWORD)  # создаем экземпляр браузера
    if not ps_pars.is_logged_in_func():  # проверяем, залогинены ли мы
        ps_pars.login()  # если нет, то логинимся
    friends_count = ps_pars.friends_count_func(ps_pars.username)  # получаем кол-во кол-во друзей
    print(friends_count)  # выводим кол-во друзей
    for user in range(1, friends_count):
        try:
            if ps_pars.psn_status(user.psn_id) == 'Добавить Друга':
                sleeptime = random.randrange(3, 10)
                await asyncio.sleep(sleeptime)
                ps_pars.add_to_friend(user.psn_id)
                await message.answer(str('запрос добавления ' + user.psn_id + ' в друзья направлен'))
            else:
                await message.answer('запрос на добавление ' + user.psn_id + ' в друзья не отправлен')
        except:
            pass



