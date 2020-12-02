"""
Хэндлеры, обращающиеся к БД, позволяющие CRUD
"""
from misc import dp
from alchemy import Person, TG_Account, DB
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
# from .handler_3_cod_stats import show_profile
from re import compile
import logging
from .handler_0_middleware import update_tg_account, full_profile_info, mentioned_user_list, zaglushka, profile_info
from datetime import datetime
from config import ADMIN_ID, COD_CHAT_ID
from aiogram import types
from .cancel_handler import cancel_handler

logger = logging.getLogger(__name__)

available_chose_edition = [
    "activision id",
    "psn id",
    "имя или прозвище"]


class OrderAddUser(StatesGroup):
    waiting_for_enter_activision_id = State()


class OrderEditUser(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()


# Редактирование пользователя. ШАГ 1. Представление
@dp.message_handler(chat_type=['private'], commands=['edit_me'], state="*")
@dp.message_handler(user_id=ADMIN_ID, commands=['edit_me'], state="*")
async def edit_me_in_bd(message: types.Message, state: FSMContext):
    logger.info(
        f'Хэндлер edit_me запущен пользователем с id {message.from_user.id} '
        f'({message.from_user.full_name}, {message.from_user.username})')
    await types.ChatActions.typing()
    db = DB()
    update_tg_account(message.from_user)
    if db.is_tg_account_exists(message.from_user.id) is False:
        await message.answer(
            str(message.from_user.first_name) + ", для выполнения данной команды вы должны зарегистрироваться." +
            "\nДля регистрации напишите боту в ПРИВАТНОМ ЧАТЕ команду: /add_me"
            )
    else:
        tg_account = db.get_tg_account(tg_id=message.from_user.id)
        person = db.get_person_by_tg_account(tg_account=tg_account)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        full_text = full_profile_info(person)
        logger.info(person)
        await message.answer(full_text, reply_markup=keyboard)
    await OrderEditUser.step_2.set()
    await message.answer(zaglushka())  # временно
    await state.finish()  # временно


# Редактирование пользователя. ШАГ 1. Представление (случай, если кого-то упомянули)
@dp.message_handler(user_id=ADMIN_ID, commands=['edit_person'], state="*")
async def edit_person_in_bd(message: types.Message, state: FSMContext):
    logger.info(
        f'Хэндлер edit_person запущен пользователем с id {message.from_user.id} '
        f'({message.from_user.full_name}, {message.from_user.username})')
    await types.ChatActions.typing()
    persons = mentioned_user_list(message)
    print('Кол-во идентифицированных упомянутых пользователей: ', len(persons))
    if len(persons) == 0:
        db = DB()
        update_tg_account(message.from_user)
        if db.is_tg_account_exists(message.from_user.id) is False:
            await message.answer(
                str(message.from_user.first_name) + ", для выполнения данной команды вы должны зарегистрироваться." +
                "\nДля регистрации напишите боту в ПРИВАТНОМ ЧАТЕ команду: /add_me"
            )
            return
        else:
            tg_account = db.get_tg_account(tg_id=message.from_user.id)
            person = db.get_person_by_tg_account(tg_account=tg_account)
        logger.info(f'В текстесообщения  не найдено упоминаний людей, ранее зарегистрированных в базе данных.')
        await message.reply('В тексте сообщения не найдено упоминаний людей, ранее зарегистрированных в базе данных.')
        await message.answer('Вывожу информацию о тебе...')
    elif len(persons) == 1:
        person = persons[0]
        logger.info(f'В тексте сообщения найдено упоминание пользователя, ранее зарегистрированного в базе данных')
        await message.reply('В тексте сообщения найдено упоминание пользователя, ранее зарегистрированного в базе данных')
        await message.answer('Вывожу информацию об этом пользователе...')
    else:
        person = persons[0]
        logger.info(f'В тексте найдено сообщения упоминание нескольких пользователей, ранее зарегистрированных в базе данных, начато редактирование пользователя {person.tg_account}')
        await message.reply(f'В тексте найдено сообщения упоминание нескольких пользователей, ранее зарегистрированных в базе данных')
        await message.answer(f'Вывожу информацию об этом пользователе...{person.tg_account}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    full_text = profile_info(person)
    logger.info(person)
    await state.update_data(person=person)
    await message.answer(full_text, reply_markup=keyboard)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Да")
    keyboard.add("Нет")

    await message.answer(f'Хотите начать редактирование данного пользователя? Да/Нет', reply_markup=keyboard)
    await OrderEditUser.step_2.set()

    # try:
        #     db.session.add(person)
        #     db.session.commit()
        #     await message.answer(
        #         str(message.from_user.first_name) + ", спасибо за регистрацию." +
        #         "\nДля внесения изменений воспользуйтесь командой: /edit_me"
        #     )
        # except Exception as ex:
        #     db.session.rollback()
        #     logger.error(ex)
        # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # keyboard.add("отмена")
        # await message.answer(
        #     "Для правильной работы сообщите мне ACTIVISION_ID:\n" +
        #     "\nпример: Ivan_Ivanov#123456789"
        #     , reply_markup=keyboard)
        # await OrderAddUser.waiting_for_enter_activision_id.set()


available_chose_to_edit = [
            "Имя(прозвище)",
            "Аккаунт ACTIVISION",
            "Аккаунт PSN",
            "Аккаунт Blizzard",
            "Аккаунт Xbox",
            "Предпочитаемая платформа",
            "Предпочитаемое устройство ввода"
            "Информация о себе"
        ]


# Редактирование пользователя. ШАГ 2. Заглушка
@dp.message_handler(state=OrderEditUser.step_2, content_types=types.ContentTypes.TEXT)
async def edit_person_step_2(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
    await types.ChatActions.typing()
    person = await state.get_data()
    if message.text.lower() == 'нет':
        print('Вы сказали НЭТ')
        await cancel_handler(message, state)
    elif message.text.lower() == 'да':
        print('Вы сказали ДАА')
        await cancel_handler(message, state)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for chose in available_chose_to_edit:
            keyboard.add(chose)
        await message.answer(f'Какие данные вы хотите указать/отредактировать?', reply_markup=keyboard)
        await OrderEditUser.step_2.set()
    else:
        await message.answer(f'Напишите или ДА, или НЕТ!!!')
        return


# Редактирование пользователя. ШАГ 3.
@dp.message_handler(state=OrderEditUser.step_3, content_types=types.ContentTypes.TEXT)
async def edit_person_step_3(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
    await types.ChatActions.typing()
    person = await state.get_data()
    if message.text.lower() == 'нет':
        print('Вы сказали НЭТ')
        await cancel_handler(message, state)
    elif message.text.lower() == 'да':
        print('Вы сказали ДАА')
        await cancel_handler(message, state)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for chose in available_chose_to_edit:
            keyboard.add(chose)
        await message.answer(f'Какие данные вы хотите указать/отредактировать?', reply_markup=keyboard)
        await OrderEditUser.step_2.set()
    else:
        await message.answer(f'Напишите или ДА, или НЕТ!!!')
        return

    # print('Выводим заглушку')
    # await message.answer(zaglushka())
    # await state.finish()

    # db = DB()
    #
    # db.get_tg_account(tg_id=message.from_user.id)
    # member = Person()
    #
    # if (message.from_user.id) is not False:
    #     member = get_member_old(message.from_user.id)
    # else:
    #     member.tg_account.id = message.from_user.id
    # await state.update_data(Activision_ID=message.text)
    # user_data = await state.get_data()
    # print(f'{user_data=}')
    #
    # pattern = compile('.+#+\d{0,20}')
    # is_valid = pattern.match(user_data['Activision_ID'])
    # if is_valid:
    #     member.activision_id = user_data['Activision_ID']
    #     session.add(member)
    #     session.commit()
    #     print(member)
    #     print('Данные прошли валидацию')
    #     await message.reply(
    #         message.from_user.first_name + ", благодарим за регистрацию!\n" +
    #         "для внесения дополнительной информации о себе советуем воспользоваться командой /edit_me",
    #         reply_markup=types.ReplyKeyboardRemove()
    #         )
    # else:
    #     print('Данные не прошли валидацию')
    #     await message.reply(message.from_user.first_name +
    #                         ", указанный вами Activision ID (" + user_data['Activision_ID'] +
    #                         ") НЕ ПРОШЁЛ ВАЛИДАЦИЮ И НЕ БЫЛ СОХРАНЁН!\n\n" +
    #                         "ещё одна попытка?! /add_me", reply_markup=types.ReplyKeyboardRemove()
    #                         )
    # await state.finish()


# # Команда редактирования пользователя. ШАГ 1. Выбор, какой параметр редактировать
# @dp.message_handler(chat_type=['private'], commands=['edit_me'], state="*")
# async def edit_user_profile_step_1(message: types.Message):
#     if is_row_exists_old(message.from_user.id) is False:
#         await message.answer(
#             str(message.from_user.first_name) + ", вы не зарегистрированы." +
#             "\nДля регистрации воспользуйтесь командой: /add_me"
#             )
#     else:
#         await show_profile(message, False)
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         for chose in available_chose_edition:
#             keyboard.add(chose.upper())
#         keyboard.add("отмена")
#         await message.answer(
#             "Вы можете указать/отредактировать следующие данные:\n\n" +
#             "ACTIVISION_ID - необьходим для работы БОТА \nпример: Ivan#123456789\n\n" +
#             "PSN_ID - для добавления в ТУСОВКУ, \nпример: Ivan_Ivanov_1999\n\n" +
#             "ИМЯ или ПРОЗВИЩЕ - для того, чтобы к вам могли обращаться по имени, \nпример: Просто Иван\n\n\n" +
#             "указание другого параметра приведёт к отмене редактирования"
#             , reply_markup=keyboard)
#         await OrderEditUser.waiting_for_choose_parameter.set()
#
#
# # Команда редактирования пользователя. ШАГ 2. Уточняем значение того параметра, что указали ранее...
# @dp.message_handler(state=OrderEditUser.waiting_for_choose_parameter, content_types=types.ContentTypes.TEXT)
# async def edit_user_profile_step_2(message: types.Message, state: FSMContext):
#     await message.reply("введите", reply_markup=types.ReplyKeyboardRemove())
#     selected_choose = message.text.lower()
#
#     if selected_choose in available_chose_edition:
#         await state.update_data(user_choose=message.text.lower())
#         user_data = await state.get_data()
#         print(f'{user_data=}')
#         await OrderEditUser.waiting_for_choose_data.set()
#     else:
#         await cancel_handler(message, state)
#         # await state.finish()
#         # await message.reply("отмена", reply_markup=types.ReplyKeyboardRemove())
#         # return
#
#
# # Команда редактирования пользователя. ШАГ 3. Сохраняем введенное значение...
# @dp.message_handler(state=OrderEditUser.waiting_for_choose_data, content_types=types.ContentTypes.TEXT)
# async def edit_user_profile_step_3(message: types.Message, state: FSMContext):
#     member = COD_User_old(tg_id=message.from_user.id)
#     if get_member_old(message.from_user.id) is not False:
#         member = get_member_old(message.from_user.id)
#     pattern = compile('')
#     user_data = await state.get_data()
#     if user_data['user_choose'] == 'activision_id':
#         pattern = compile('.+#+\d{0,20}')
#     if user_data['user_choose'] == 'psn id':
#         pattern = compile('\w')
#     if user_data['user_choose'] == 'имя или прозвище':
#         pattern = compile('\w')
#     is_valid = pattern.match(user_data['user_choose'])
#     await state.update_data(value=message.text)
#     user_data = await state.get_data()
#     print(f'{user_data=}')
#     if is_valid:
#         if user_data['user_choose'] == 'activision id':
#             member.activision_id = user_data['value']
#         if user_data['user_choose'] == 'psn id':
#             member.psn_id = user_data['value']
#         if user_data['user_choose'] == 'имя или прозвище':
#             member.name = user_data['value']
#         session.add(member)
#         session.commit()
#         await message.reply(
#             message.from_user.first_name + ", вы выбрали обновить " + user_data['user_choose'] +
#             " и указали значение " + user_data['value'], reply_markup=types.ReplyKeyboardRemove()
#             )
#     else:
#         await message.reply(
#             message.from_user.first_name + ", вы выбрали обновить " + user_data['user_choose'] +
#             " и указали значение " + user_data['value'] + "\n\n"
#             "УКАЗАННЫЕ ВАМИ ДАНЫЕ НЕ ПРОШЛИ ВАЛИДАЦИЮ И НЕ БЫЛИ СОХРАНЕНЫ!", reply_markup=types.ReplyKeyboardRemove()
#             )
#     await OrderEditUser.waiting_for_continue_editing.set()
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add("Продолжить редактирование")
#     keyboard.add("Завершить редактирование")
#     await message.answer(
#         "Продолжить редактирование профиля?\n\n", reply_markup=keyboard)
#
#
# # Команда редактирования пользователя. ШАГ 4. Продолжить или прервать редактирование?
# @dp.message_handler(state=OrderEditUser.waiting_for_continue_editing, content_types=types.ContentTypes.TEXT)
# async def edit_user_profile_step_4(message: types.Message, state: FSMContext):
#     if message.text == "Продолжить редактирование":
#         await edit_user_profile_step_1(message)
#     else:
#         await state.finish()
#         await message.reply("Редактирование профиля завершено", reply=True, reply_markup=types.ReplyKeyboardRemove())
#         return
#
#
