from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import asyncio
import keyboars
from handlers.carrier import router as carrier_router
from handlers.driver import router as driver_router
from handlers.logout import router as logout_router
from handlers.search import router as search_roter
from handlers.base import router as base_router
from handlers.admin import router as admin_router
from aiogram.types import *
from db import *
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(base_router)
dp.include_router(admin_router)
dp.include_router(carrier_router)
dp.include_router(driver_router)
dp.include_router(logout_router)
dp.include_router(search_roter)

# Start command handler
@dp.message(Command("start"))
async def welcome(message: Message):
    # await message.delete()
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        await message.answer("You are admin!, Welcome...", reply_markup=keyboars.admin_menu)
        return

    company = await get_by_id(user_id, "companies")

    if company:
        await message.answer("Welcome...", reply_markup=keyboars.carrier_main_menu)
        return
    
    driver = await get_by_id(user_id, "drivers")
    if driver:
        await message.answer("Welcome...", reply_markup=keyboars.driver_main_menu)
        return

    await message.reply(
        "Welcome!, Please choose how you want to register:",
        reply_markup=keyboars.register_keyboard
    )

@dp.message(F.text == "Cancel⬅️")
async def cancel(message: Message, state: FSMContext):
    if state:
        await state.clear()
        
    user_id = message.from_user.id
    
    if user_id in config.ADMINS:
        await message.answer("Cancelled...", reply_markup=keyboars.admin_menu)
        return
    
    company = await get_by_id(user_id, "companies")

    if company:
        await message.answer("Cancelled...", reply_markup=keyboars.carrier_main_menu)
        return
    
    driver = await get_by_id(user_id, "drivers")
    if driver:
        await message.answer("Cancelled...", reply_markup=keyboars.driver_main_menu)
        return
    
    await message.answer("Cancelled...", reply_markup=keyboars.register_keyboard)


async def main():
    print("Starting....")
    await  dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())