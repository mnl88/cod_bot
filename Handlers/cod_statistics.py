import config
from aiogram import types
from misc import dp
from alchemy import *
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from cod_stats_parser import *
import asyncio
from . import new_handler as new
from re import *

user_commands_list = '/add_me - add_me,\n' \
                     '/update_my_account - update_my_account,\n' \
                     '/delete_me - delete_me,\n'

admin_commands_list = ''


session = db_init()
available_chose = [
    "activision id",
    "psn id",
    "имя или прозвище",
    "отмена"]


class OrderSetId(StatesGroup):
    waiting_for_choose_id = State()
    upgrade_id_in_bd = State()


# Команда добавления пользователя
@dp.message_handler(commands=['add_me'])
async def add_user_to_bd(message: types.Message):
    if is_row_exists(session, message.from_user.id):
        member = get_member(session, message.from_user.id)
        await message.answer(str(message.from_user.first_name) + ", вы уже были зарегистрированы ранее")
        await new.show_my_stats(message)

    else:  # если юзера нет в базе, добавляем его
        member = add_member(session, message.from_user.id, message.from_user.username)
        await message.answer(str(message.from_user.first_name) + ", добро пожаловать в клуб!")
    await update_my_profile_step_1(message)
    print(member)


# Команда обновления связанных с пользователем учеток. ШАГ 1
@dp.message_handler(commands="update_my_account", state="*")
async def update_my_profile_step_1(message: types.Message):
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
async def update_my_profile_step_2(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
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
async def update_my_profile_step_3(message: types.Message, state: FSMContext):
    me = get_member(session, message.from_user.id)
    await state.update_data(value=message.text)
    user_data = await state.get_data()
    print(user_data)

    pattern = compile('\w+#+\d{0,20}')
    if user_data['user_choose'] == 'activision_id':
        pattern = compile('\w+#+\d{0,20}')
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
            me.activision_id = user_data['value']
        if user_data['user_choose'] == 'psn id':
            me.psn_id = user_data['value']
        if user_data['user_choose'] == 'имя или прозвище':
            me.name = user_data['value']
        session.add(me)
        session.commit()
        print(me)
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
