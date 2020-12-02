# точка входа
from aiogram import executor
from misc import dp
import Handlers
# import Handlers_not_ready

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
