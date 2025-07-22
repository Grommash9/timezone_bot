import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN
from handlers import cmd_settz, cmd_settz_for, cmd_listtz, handle_time_mentions
from db import init_db

async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(cmd_settz, Command("settz"))
    dp.message.register(cmd_settz_for, Command("settz_for"))
    dp.message.register(cmd_listtz, Command("listtz"))
    dp.message.register(handle_time_mentions)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
