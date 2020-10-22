"""
Хэндлеры, обращающиеся к БД, позволяющие CRUD
"""

from misc import dp
from alchemy import session
from alchemy import is_row_exists, get_member, add_member, get_all_members, datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .handler_3_cod_stats import show_profile, show_stats
from cod_stats_parser import parser_act_id
import asyncio
from re import *


available_chose = [
    "activision id",
    "psn id",
    "имя или прозвище",
    "отмена"]


class OrderSetId(StatesGroup):
    waiting_for_choose_id = State()
    upgrade_id_in_bd = State()


# Команда добавления пользователя. ШАГ 1
@dp.message_handler(commands=['add_me'], state="*")
async def add_user_to_bd(message: types.Message):
    if is_row_exists(message.from_user.id):
        await message.answer(
            str(message.from_user.first_name) + ", вы уже были зарегистрированы ранее." +
            "\nДля внесения изменений воспользуйтесь командой: /edit_me"
            )
        await show_profile(message, False)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for chose in available_chose:
            keyboard.add(chose.upper())
        await message.answer(
            "Для правильной работы БОТА трубется указать следующие данные:\n\n" +
            "ACTIVISION_ID - ОБЯЗАТЕЛЬНО, \nпример: Ivan#123456789 \n\n" +
            "PSN_ID - необязательно, нужно для добавления в ТУСОВКУ, \nпример: Ivan_Ivanov_1999 \n\n" +
            "ИМЯ или ПРОЗВИЩЕ - необязательно, нужно для того, чтобы к вам могли обращаться по имени, \nпример: Иван \n"
            , reply_markup=keyboard)
        await OrderSetId.waiting_for_choose_id.set()


# Команда обновления связанных с пользователем учеток. ШАГ 2
@dp.message_handler(state=OrderSetId.waiting_for_choose_id, content_types=types.ContentTypes.TEXT)
async def add_user_to_bd_step_2(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
    if message.text.lower() not in available_chose:
        await message.reply("Пожалуйста, сделайте выбор, используя клавиатуру ниже.")
        return
    if message.text.lower() == 'отмена':
        await state.finish()
        await message.reply("есть отмена!!!", reply_markup=types.ReplyKeyboardRemove())
        return
    await state.update_data(user_choose=message.text.lower())
    await OrderSetId.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    user_data = await state.get_data()
    print(user_data)
    await message.reply("напишите " + user_data['user_choose'], reply_markup=types.ReplyKeyboardRemove())


# Команда обновления связанных с пользователем учеток. ШАГ 3
@dp.message_handler(state=OrderSetId.upgrade_id_in_bd, content_types=types.ContentTypes.TEXT)
async def add_user_to_bd_step_3(message: types.Message, state: FSMContext):
    member = get_member(message.from_user.id)
    await state.update_data(value=message.text)
    user_data = await state.get_data()
    print(user_data)

    pattern = compile('')
    if user_data['user_choose'] == 'activision_id':
        pattern = compile('.+#+\d{0,20}')
    if user_data['user_choose'] == 'psn id':
        pattern = compile('\w')
    if user_data['user_choose'] == 'имя или прозвище':
        pattern = compile('\w')
    is_valid = pattern.match(user_data['value'])

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for chose in available_chose:
        keyboard.add(chose.upper())

    if is_valid:
        if user_data['user_choose'] == 'activision id':
            member.activision_id = user_data['value']
        if user_data['user_choose'] == 'psn id':
            member.psn_id = user_data['value']
        if user_data['user_choose'] == 'имя или прозвище':
            member.name = user_data['value']
        session.add(member)
        session.commit()
        print(member)
        print('Данные прошли валидацию')
        await message.reply(message.from_user.first_name +
                            ", вы выбрали обновить " + user_data['user_choose'] +
                            " и указали значение " + user_data['value'] +
                            ".\n\nХотите ещё что-то добавить/изменить?", reply_markup=keyboard
                            )

    else:
        print('Данные не прошли валидацию')
        await message.reply(message.from_user.first_name +
                            ", вы выбрали обновить " + user_data['user_choose'] +
                            " и указали значение " + user_data['value'] +
                            "\n\nУКАЗАННЫЕ ВАМИ ДАНЫЕ НЕ ПРОШЛИ ВАЛИДАЦИЮ И НЕ БЫЛИ СОХРАНЕНЫ!\n" +
                            "Хотите что-то добавить/изменить?", reply_markup=keyboard
                            )
    await OrderSetId.first()


# Обновление статистики по КД
@dp.message_handler(commands=['update_stat'])
async def update_me(message: types.Message):
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


# Обновление всем статистики
@dp.message_handler(commands=['update_all'])
async def update_all(message: types.Message):
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



# Команда редактирования пользователя
@dp.message_handler(commands=['edit_me'])
async def edit_user_in_bd(message: types.Message):
    if is_row_exists(message.from_user.id):
        member = get_member(message.from_user.id)
        await message.answer(str(message.from_user.first_name) + ", вы уже были зарегистрированы ранее")
        await show_stats(message)

    else:  # если юзера нет в базе, добавляем его
        member = add_member(message.from_user.id, message.from_user.username)
        await message.answer(str(message.from_user.first_name) + ", добро пожаловать в клуб!")
    await(message)

    print(member)





# Команда отписки
# @dp.message_handler(commands=['delete_me'])
# async def delete_member(message: types.Message):
#     if not db.member_exists(message.from_user.id):
#         # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
#         db.add_member(message.from_user.id, message.from_user.username, False)
#         await message.answer("Вы даже к нам не заходили!")
#     else:
#         # если он уже есть, то просто обновляем ему статус подписки
#         db.update_member(message.from_user.id, False)
#         await message.answer("Что ж, прощай, бывший друг!!!")
