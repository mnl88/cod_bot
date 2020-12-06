# точка входа
from aiogram import executor
from misc import dp
import Handlers_not_ready
import Handlers


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
