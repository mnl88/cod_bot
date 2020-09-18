import asyncio
import datetime
import config
from aiogram import types
from misc import dp
from alchemy import *
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from cod_stats_parser import *
#
# available_choose = [
#     "старт",
#     "стоп",
#     "отмена"]
#
#
# class Schedule_state(StatesGroup):
#     schedule_on = State()
#     schedule_on22 = State()
#
#
# @dp.message_handler(user_id=config.ADMIN_ID, commands="schedule")
# async def schedule(message: types.Message):
#     print('def schedule')
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     for choose in available_choose:
#         keyboard.add(choose.lower())
#     await message.answer(
#         "Старт, стоп или отмена?", reply_markup=keyboard)
#     await Schedule_state.schedule_on22.set()
#     await schedule_set(message)
#
#
# @dp.message_handler(state=Schedule_state.schedule_on.set(), content_types=types.ContentTypes.TEXT)
# async def schedule_set(message: types.Message, state: FSMContext):
#     print('def schedule set')
#     if message.text.lower() not in available_choose:
#         await message.reply("Пожалуйста, сделайте выбор, используя клавиатуру ниже.")
#         return
#     if message.text.lower() == 'отмена':
#         await state.finish()
#         await message.reply("есть отмена!!!", reply_markup=types.ReplyKeyboardRemove())
#         return
#     await state.update_data(command=message.text.lower())
#     await Schedule_state.next()  # для простых шагов можно не указывать название состояния, обходясь next()
#     user_data = await state.get_data()
#     print(user_data)
#     await message.reply("напишите " + user_data['user_choose'], reply_markup=types.ReplyKeyboardRemove())
#
#
# @dp.message_handler(commands="infinity")
# async def schedule_set(message: types.Message, state: FSMContext):
#     while True:
#         await asyncio.sleep(3)
#         if await state.get_data() == "старт":
#             print('раз-два-три')

import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor


# States
class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'


@dp.message_handler(commands='abc')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.name.set()

    await message.reply("Hi there! What's your name?")


# You can use state '*' if you need to handle all states
@dp.message_handler(state=[Form.name, Form.age, Form.gender], commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state=[Form.name, Form.age, Form.gender])
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    await state.update_data(name=str(message.text))

    await Form.next()
    await message.reply("How old are you?")


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    """
    If age is invalid
    """
    return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(age=int(message.text))

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Male", "Female")
    markup.add("Other")

    await message.reply("What is your gender?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender)
async def process_gender_invalid(message: types.Message):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    return await message.reply("Bad gender name. Choose your gender from the keyboard.")


@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=str(message.text))

    # Remove keyboard
    markup = types.ReplyKeyboardRemove()
    user_data = await state.get_data()
    # And send message
    await message.answer(text="Hi! Nice to meet you" + str(user_data['name']), reply_markup=markup)
    # Finish conversation
    await state.finish()


