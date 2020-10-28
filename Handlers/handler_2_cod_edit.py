"""
Хэндлеры, обращающиеся к БД, позволяющие CRUD
"""

from misc import dp
from alchemy import session
from alchemy import is_row_exists, get_member, COD_User
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from .handler_3_cod_stats import show_profile
from re import compile
from config import COD_CHAT_ID


available_chose_edition = [
    "activision id",
    "psn id",
    "имя или прозвище"]


class OrderAddUser(StatesGroup):
    waiting_for_enter_activision_id = State()


class OrderEditUser(StatesGroup):
    waiting_for_choose_parameter = State()
    waiting_for_choose_data = State()
    waiting_for_continue_editing = State()


# Прервать любой их Хэндлеров
@dp.message_handler(state='*', commands=['cancel', 'отмена'])
@dp.message_handler(Text(equals=['cancel', 'отмена'], ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


# Команда добавления пользователя. ШАГ 1
@dp.message_handler(chat_id=COD_CHAT_ID, commands=['add_me'], state="*")
async def add_user_to_bd_step_1(message: types.Message):
    if is_row_exists(message.from_user.id):
        await message.answer(
            str(message.from_user.first_name) + ", вы уже были зарегистрированы ранее." +
            "\nДля внесения изменений воспользуйтесь командой: /edit_me"
            )
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("отмена")
        await message.answer(
            "Для правильной работы сообщите мне ACTIVISION_ID:\n" +
            "\nпример: Ivan_Ivanov#123456789"
            , reply_markup=keyboard)
        await OrderAddUser.waiting_for_enter_activision_id.set()


# Команда добавления пользователя. ШАГ 2
@dp.message_handler(state=OrderAddUser.waiting_for_enter_activision_id, content_types=types.ContentTypes.TEXT)
async def add_user_to_bd_step_2(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
    member = COD_User(tg_id=message.from_user.id)
    if get_member(message.from_user.id) is not False:
        member = get_member(message.from_user.id)
    await state.update_data(Activision_ID=message.text)
    user_data = await state.get_data()
    print(f'{user_data=}')

    pattern = compile('.+#+\d{0,20}')
    is_valid = pattern.match(user_data['Activision_ID'])
    if is_valid:
        member.activision_id = user_data['Activision_ID']
        session.add(member)
        session.commit()
        print(member)
        print('Данные прошли валидацию')
        await message.reply(
            message.from_user.first_name + ", благодарим за регистрацию!\n" +
            "для внесения дополнительной информации о себе советуем воспользоваться командой /edit_me",
            reply_markup=types.ReplyKeyboardRemove()
            )
    else:
        print('Данные не прошли валидацию')
        await message.reply(message.from_user.first_name +
                            ", указанный вами Activision ID (" + user_data['Activision_ID'] +
                            ") НЕ ПРОШЁЛ ВАЛИДАЦИЮ И НЕ БЫЛ СОХРАНЁН!\n\n" +
                            "ещё одна попытка?! /add_me", reply_markup=types.ReplyKeyboardRemove()
                            )
    await state.finish()


# Команда редактирования пользователя. ШАГ 1. Выбор, какой параметр редактировать
@dp.message_handler(chat_id=COD_CHAT_ID, commands=['edit_me'], state="*")
async def edit_user_profile_step_1(message: types.Message):
    if is_row_exists(message.from_user.id) is False:
        await message.answer(
            str(message.from_user.first_name) + ", вы не зарегистрированы." +
            "\nДля регистрации воспользуйтесь командой: /add_me"
            )
    else:
        await show_profile(message, False)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for chose in available_chose_edition:
            keyboard.add(chose.upper())
        keyboard.add("отмена")
        await message.answer(
            "Вы можете указать/отредактировать следующие данные:\n\n" +
            "ACTIVISION_ID - необьходим для работы БОТА \nпример: Ivan#123456789\n\n" +
            "PSN_ID - для добавления в ТУСОВКУ, \nпример: Ivan_Ivanov_1999\n\n" +
            "ИМЯ или ПРОЗВИЩЕ - для того, чтобы к вам могли обращаться по имени, \nпример: Просто Иван\n\n\n" +
            "указание другого параметра приведёт к отмене редактирования"
            , reply_markup=keyboard)
        await OrderEditUser.waiting_for_choose_parameter.set()


# Команда редактирования пользователя. ШАГ 2. Уточняем значение того параметра, что указали ранее...
@dp.message_handler(state=OrderEditUser.waiting_for_choose_parameter, content_types=types.ContentTypes.TEXT)
async def edit_user_profile_step_2(message: types.Message, state: FSMContext):
    await message.reply("введите", reply_markup=types.ReplyKeyboardRemove())
    selected_choose = message.text.lower()

    if selected_choose in available_chose_edition:
        await state.update_data(user_choose=message.text.lower())
        user_data = await state.get_data()
        print(f'{user_data=}')
        await OrderEditUser.waiting_for_choose_data.set()
    else:
        await cancel_handler(message)
        # await state.finish()
        # await message.reply("отмена", reply_markup=types.ReplyKeyboardRemove())
        # return


# Команда редактирования пользователя. ШАГ 3. Сохраняем введенное значение...
@dp.message_handler(state=OrderEditUser.waiting_for_choose_data, content_types=types.ContentTypes.TEXT)
async def edit_user_profile_step_3(message: types.Message, state: FSMContext):
    member = COD_User(tg_id=message.from_user.id)
    if get_member(message.from_user.id) is not False:
        member = get_member(message.from_user.id)
    pattern = compile('')
    user_data = await state.get_data()
    if user_data['user_choose'] == 'activision_id':
        pattern = compile('.+#+\d{0,20}')
    if user_data['user_choose'] == 'psn id':
        pattern = compile('\w')
    if user_data['user_choose'] == 'имя или прозвище':
        pattern = compile('\w')
    is_valid = pattern.match(user_data['user_choose'])
    await state.update_data(value=message.text)
    user_data = await state.get_data()
    print(f'{user_data=}')
    if is_valid:
        if user_data['user_choose'] == 'activision id':
            member.activision_id = user_data['value']
        if user_data['user_choose'] == 'psn id':
            member.psn_id = user_data['value']
        if user_data['user_choose'] == 'имя или прозвище':
            member.name = user_data['value']
        session.add(member)
        session.commit()
        await message.reply(
            message.from_user.first_name + ", вы выбрали обновить " + user_data['user_choose'] +
            " и указали значение " + user_data['value'], reply_markup=types.ReplyKeyboardRemove()
            )
    else:
        await message.reply(
            message.from_user.first_name + ", вы выбрали обновить " + user_data['user_choose'] +
            " и указали значение " + user_data['value'] + "\n\n"
            "УКАЗАННЫЕ ВАМИ ДАНЫЕ НЕ ПРОШЛИ ВАЛИДАЦИЮ И НЕ БЫЛИ СОХРАНЕНЫ!", reply_markup=types.ReplyKeyboardRemove()
            )
    await OrderEditUser.waiting_for_continue_editing.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Продолжить редактирование")
    keyboard.add("Завершить редактирование")
    await message.answer(
        "Продолжить редактирование профиля?\n\n", reply_markup=keyboard)


# Команда редактирования пользователя. ШАГ 4. Продолжить или прервать редактирование?
@dp.message_handler(state=OrderEditUser.waiting_for_continue_editing, content_types=types.ContentTypes.TEXT)
async def edit_user_profile_step_4(message: types.Message, state: FSMContext):
    if message.text == "Продолжить редактирование":
        await edit_user_profile_step_1(message)
    else:
        await state.finish()
        await message.reply("Редактирование профиля завершено", reply=True, reply_markup=types.ReplyKeyboardRemove())
        return


