from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db import *
import keyboars
from .functions import *
from config import USER_ACTIVITY
from datetime import datetime

router = Router()

class LogOut(StatesGroup):
    Answer = State()

@router.message(F.text == "Delete Account❌")
async def startLogOut(message: types.Message, state: FSMContext):
    try:
        USER_ACTIVITY[message.from_user.id] = datetime.now()
        await state.set_state(LogOut.Answer)
        await message.answer("You sure that, if you log out your all data will be deleted? ", reply_markup=keyboars.yes_no)
    except:
        await message.answer("Something went wrong, /start and try again")

@router.message(LogOut.Answer)
async def LogOutIfUsersAnswerIsYes(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        await state.update_data(answer=message.text)
        data = await state.get_data()
        if data['answer'] == "YES I'M SURE":
            await message.answer("Erasing...", reply_markup=types.ReplyKeyboardRemove())
            await deleteAllData(user_id=user_id)
            await message.answer("Done!", reply_markup=keyboars.register_keyboard)

        await state.clear()
    except:
        await message.answer("Something went wrong, /start and try again", reply_markup=keyboars.register_keyboard)


