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
from handlers.base import UpdateBalances
from handlers.admin import router as admin_router
from aiogram.types import *
from db import *
import config
from handlers.functions import *
from aiogram.fsm.state import StatesGroup, State
from bot_instance import bot, dp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

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

class SupportState(StatesGroup):
    Message = State()


@dp.message(F.text == "Support🔧")
async def handle_support(message: Message, state: FSMContext):
    try:
        await state.set_state(SupportState.Message)
        await message.answer("Enter a message to send to admin", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something wrong, Please try again.")

@dp.message(SupportState.Message)
async def sendtoAdmin(message: Message, state: FSMContext):
    try:
        await state.update_data(message=message.text)
        data = await state.get_data()
        await state.clear()
        user_id = message.from_user.id
        user_link = f"tg://user?id={user_id}"
        for adminId in config.ADMINS:
            await bot.send_message(adminId, f"✍️User: <a href='{user_link}'>{user_id}</a>\nMessage: {data['message']}", parse_mode="HTML")

        driver = await get_by_id(user_id, "drivers")
        if driver:
            await message.answer("Sent to admin!", reply_markup=keyboars.driver_main_menu)
        else:
            await message.answer("Sent to admin!", reply_markup=keyboars.carrier_main_menu)
    except Exception as ex:
        print(ex)
        await message.answer("Something wrong, Please try again.")


async def main():
    scheduler = AsyncIOScheduler(timezone=timezone("Asia/Tashkent"))
    scheduler.add_job(UpdateBalances, CronTrigger(hour=23, minute=57, timezone=timezone("Asia/Tashkent")))
    scheduler.start()
    print("Starting....")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())