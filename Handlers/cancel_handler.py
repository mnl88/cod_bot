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
from datetime import datetime


logger = logging.getLogger(__name__)


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