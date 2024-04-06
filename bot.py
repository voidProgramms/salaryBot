import asyncio
import logging
import sys
from os import getenv


from aiogram import Bot, Dispatcher

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from handlers.salaryHandler import main_router

ALLOWED = ['message', 'callback_query']

TOKEN = getenv('TOKEN')

dp = Dispatcher()
dp.include_router(main_router)


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot, allowed_updates=ALLOWED)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

