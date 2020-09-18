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




# available_choose = (
#     ('CTAPT', 'on'),
#     ('CТОП', 'off'),
# )

available_choose = [
    "старт",
    "стоп",
    "отмена"]


class Spam_status(StatesGroup):
    spam_unsigned = State()
    spam_on = State()
    spam_off = State()


@dp.message_handler(user_id=config.ADMIN_ID, commands="spam")
async def spam(message: types.Message):
    print('spam')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for choose in available_choose:
        keyboard.add(choose.lower())
    await message.answer(
        "Старт, стоп или отмена?", reply_markup=keyboard)
    await Spam_status.spam_unsigned.set()


@dp.message_handler(state=Spam_status.spam_unsigned, content_types=types.ContentTypes.TEXT)
@dp.async_task
async def status_set(message: types.Message, state: FSMContext):
    print('status_set')
    text = f'не выбрано'
    if message.text.lower() == 'старт':
        await Spam_status.spam_on.set()
        text = f'ВКЛЮЧЕНО'
    if message.text.lower() == 'стоп':
        await Spam_status.spam_off.set()
        text = f'ВЫКЛЮЧЕНО'
    print(text)
    markup = types.ReplyKeyboardRemove()
    await message.answer(text=text, reply_markup=markup)
    while True:
        await asyncio.sleep(4)
        current_state = await state.get_state()
        print(datetime.now(), current_state)


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo(message: types.Message):
    await message.answer(message.text)


# @dp.message_handler(commands="infinity")
# async def schedule_set(message: types.Message, state: FSMContext):
#     while True:
#         await asyncio.sleep(3)
#         if await state.get_data() == "старт":
#             print('раз-два-три')
#
#
# import logging
#
# import aiogram.utils.markdown as md
# from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import ParseMode
# from aiogram.utils import executor
#
#
# # States
# class Form(StatesGroup):
#     name = State()  # Will be represented in storage as 'Form:name'
#     age = State()  # Will be represented in storage as 'Form:age'
#     gender = State()  # Will be represented in storage as 'Form:gender'
#
#
# @dp.message_handler(commands='abc')
# async def cmd_start(message: types.Message):
#     """
#     Conversation's entry point
#     """
#     # Set state
#     await Form.name.set()
#
#     await message.reply("Hi there! What's your name?")
#
#
# # You can use state '*' if you need to handle all states
# @dp.message_handler(state=[Form.name, Form.age, Form.gender], commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state=[Form.name, Form.age, Form.gender])
# async def cancel_handler(message: types.Message, state: FSMContext):
#     """
#     Allow user to cancel any action
#     """
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#
#     logging.info('Cancelling state %r', current_state)
#     # Cancel state and inform user about it
#     await state.finish()
#     # And remove keyboard (just in case)
#     await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())
#
#
# @dp.message_handler(state=Form.name)
# async def process_name(message: types.Message, state: FSMContext):
#     """
#     Process user name
#     """
#     await state.update_data(name=str(message.text))
#
#     await Form.next()
#     await message.reply("How old are you?")
#
#
# # Check age. Age gotta be digit
# @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
# async def process_age_invalid(message: types.Message):
#     """
#     If age is invalid
#     """
#     return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")
#
#
# @dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
# async def process_age(message: types.Message, state: FSMContext):
#     # Update state and data
#     await Form.next()
#     await state.update_data(age=int(message.text))
#
#     # Configure ReplyKeyboardMarkup
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#     markup.add("Male", "Female")
#     markup.add("Other")
#
#     await message.reply("What is your gender?", reply_markup=markup)
#
#
# @dp.message_handler(lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender)
# async def process_gender_invalid(message: types.Message):
#     """
#     In this example gender has to be one of: Male, Female, Other.
#     """
#     return await message.reply("Bad gender name. Choose your gender from the keyboard.")
#
#
# @dp.message_handler(state=Form.gender)
# async def process_gender(message: types.Message, state: FSMContext):
#     await state.update_data(gender=str(message.text))
#
#     # Remove keyboard
#     markup = types.ReplyKeyboardRemove()
#     user_data = await state.get_data()
#     # And send message
#     await message.answer(text="Hi! Nice to meet you" + str(user_data['name']), reply_markup=markup)
#     # Finish conversation
#     await state.finish()
#
#
