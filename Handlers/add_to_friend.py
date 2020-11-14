from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from re import compile
from misc import dp
from config import ADMIN_ID, COD_CHAT_ID, PSN_EMAIL, PSN_PASSWORD, PSN_USERNAME
from alchemy import get_all_members, COD_User
from psn_selenium_parser import PSN_Bot
import asyncio
import random
import logging


logger = logging.getLogger(__name__)

# Запускаем бот из группы
@dp.message_handler(user_id=ADMIN_ID, chat_type='private', commands=['add_all_psn_to_friends', 'aaa'])
async def add_all_psn_to_friends(message: types.Message):
    logger.info(
        f'Хэндлер ADD_ALL_PSN_TO_FRIEND запущен пользователем с id {message.from_user.id} '
        f'({message.from_user.full_name}, {message.from_user.username})')
    members = get_all_members()  # получаем список всех пользователей из БД
    members_with_psn = []
    logger.info(f'Всего профилей в БД: {len(members)}')
    for user in members:
        if user.psn_id != 'unknown':
            logger.debug(f'{user} - PSN указан ({user.psn_id})')
            members_with_psn.append(user)

    logger.info(f'Всего профилей в БД c PSN: {len(members_with_psn)}')  # выводим список пользователей из БД с psn_id
    for item in members_with_psn:
        logger.info(f'профилей в БД c PSN - {item}')
    ps_pars = PSN_Bot(PSN_USERNAME, PSN_EMAIL, PSN_PASSWORD)  # создаем экземпляр браузера
    if not ps_pars.is_logged_in_func():  # проверяем, залогинены ли мы
        ps_pars.login()  # если нет, то логинимся
    psn_friends = ps_pars.friends_list(ps_pars.username)
    logger.info(f'Друзей в PSN: {len(psn_friends)}')  # выводим кол-во друзей
    i = 0
    for item in psn_friends:
        logger.info(f': {i} друг - {item}')  # выводим кол-во друзей в PSN
        i +=1
    members_with_psn_not_friend = members_with_psn
    for user in members_with_psn:
        user: COD_User
        for psn_friend in psn_friends:
            if user.psn_id == psn_friend['psn']:
                logger.info(f'найден друг с PSN: {user.psn_id}')
                members_with_psn_not_friend.remove(user)
    logger.info(
        f'Пользователей в БД, указавших PSN, но не подружившихся с ботом: {len(members_with_psn_not_friend)}')  # выводим кол-во друзей
    for member_with_psn_not_friend in members_with_psn_not_friend:
        logger.info(f'{member_with_psn_not_friend.psn_id}')


    for user in members_with_psn_not_friend:
        try:
            if ps_pars.psn_status(user.psn_id) == 'Добавить Друга':
                sleeptime = random.randrange(3, 10)
                await asyncio.sleep(sleeptime)
                ps_pars.add_to_friend(user.psn_id)
                await message.answer(str(user.psn_id + ' - направлен в друзья направлен'))
            elif ps_pars.psn_status(user.psn_id) == 'Вы подписаны':
                await message.answer('Скорее всего с пользователем ' + user.psn_id + ' вы уже друзья')
            elif ps_pars.psn_status(user.psn_id) == 'Подписаться':
                await message.answer('запрос на добавление ' + user.psn_id + ' уже был ранее отправлен')
            else:
                logging.exception("Что-то не так")
        except:
            logging.exception("Exception occurred")



