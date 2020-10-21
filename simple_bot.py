# точка входа
from aiogram import executor
import logging
import config
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


# Configure logging
# logging.basicConfig(level=logging.INFO)



#
# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#
#     await message.answer(message.text)
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)