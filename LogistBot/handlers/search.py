from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import *
from keyboars import *
import random

router = Router()

class CompanyStatus(StatesGroup):
    IsActive = State()
    CompanyDriver = State()
    OwnerDriver = State()
    LeaseDriver = State()

@router.message(F.text == "Settings⚙️")
async def start_company_status(message: types.Message, state: FSMContext):
    try:
        await message.answer('Choose your status:', reply_markup=active_passive)
        await state.set_state(CompanyStatus.IsActive)
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())
        
@router.message(CompanyStatus.IsActive)
async def ask_CompanyDriver(message: types.Message, state: FSMContext):
    try:
        if message.text.lower() != "active" and message.text.lower() != "passive":
            await message.answer("Please use buttons!")
            return
        
        await state.update_data(IsActive=message.text)
        await state.set_state(CompanyStatus.CompanyDriver)
        await message.answer("Are you looking for a company driver?", reply_markup=yesno)
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())
        
@router.message(CompanyStatus.CompanyDriver)
async def ask_OwnerDriver(message: types.Message, state: FSMContext):
    try:
        message_text = message.text
        if message_text not in ["YES", "NO"]:
            await message.answer("Please use buttons!")
            return
        
        await state.update_data(CompanyDriver=message_text)
        await state.set_state(CompanyStatus.OwnerDriver)
        await message.answer('Are you looking for a owner driver?', reply_markup=yesno)
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())
        
@router.message(CompanyStatus.OwnerDriver)
async def ask_LeaseDriver(message: types.Message, state: FSMContext):
    try:
        msg = message.text
        if msg not in ["YES", "NO"]:
            await message.answer('Plase use buttons!')
            return
        
        await state.update_data(OwnerDriver=msg)
        await state.set_state(CompanyStatus.LeaseDriver)
        await message.answer('Are you looking for a lease driver?', reply_markup=yesno)
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())
        
@router.message(CompanyStatus.LeaseDriver)
async def finish_CompantStatusState(msg: types.Message, state: FSMContext):
    try:
        txt = msg.text
        if txt not in ["YES", "NO"]:
            await msg.answer('Please use buttons!')
            return
        
        await state.update_data(LeaseDriver=txt)
        data = await state.get_data()
        data.update({'id':msg.from_user.id})
        await update_driver_filter(data=data)
        await state.clear()
        await msg.answer('OK', reply_markup=carrier_main_menu)
    except:
        await msg.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())


class DriverStatus(StatesGroup):
    IsActive = State()

@router.message(F.text == "Status⚙️")
async def ask_status(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        driver_status = await get_by_id(user_id, "DriverStatus")
        if driver_status:
            if driver_status['is_active']:
                await message.answer(f"Your current status is: Active⚡️")
            else:
                await message.answer(f"Your current status is: Passive")

        
        await state.set_state(DriverStatus.IsActive)
        await message.answer("Select your new status: ", reply_markup=active_passive)
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())
        
@router.message(DriverStatus.IsActive)
async def finish_DriverStatus(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        status = message.text.lower() == "active"
        await update_driver_status(user_id, status=status)
        await state.clear()
        await message.answer("Saved!", reply_markup=driver_main_menu)
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())


@router.message(lambda message: message.text == "Search Companies🔎")
async def driver_search(message: types.Message, state: FSMContext):
    try:
        companies = await get_all_companies()
        if not companies:
            await message.answer("No companies found!")
            return
        
        random_company = random.choice(companies)
        await state.update_data(current_company=random_company)

        await message.answer(f"Company: {random_company['company_name']}\nDOT: {random_company['dot']}\nMC: {random_company['mc']}\nAddress: {random_company['address']}\nCurrent trucks: {random_company['current_trucks']}\nEmail: {random_company['company_email']}\nContact: {random_company['company_contact']}",
                             reply_markup=driver_keyboard)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())
        

@router.callback_query(CompanyCallback.filter())
async def handleCompanyCallback(callback_query: types.CallbackQuery, callback_data: CallbackData):
    try:
        action = callback_data.action
        if action == "cancel":
            await callback_query.message.edit_text("Cancelled 🚫")
            return
        elif action == "next":
            companies = await get_all_companies()
            if not companies:
                await callback_query.answer("No companies found!")
                return
            
            # random_company = companies[random.randint(0, len(companies)-1)]
            random_company = random.choice(companies)
            await callback_query.message.edit_text(f"Company: {random_company['company_name']}\nDOT: {random_company['dot']}\nMC: {random_company['mc']}\nAddress: {random_company['address']}\nCurrent trucks: {random_company['current_trucks']}\nEmail: {random_company['company_email']}\nContact: {random_company['company_contact']}",
                                                reply_markup=driver_keyboard)
    except Exception as e:
        print(e)
        await callback_query.answer("Slow!")

@router.message(lambda message: message.text == "Search Drivers🔍")
async def search_drivers(message: types.Message, state: FSMContext):
    try:
        drivers = await get_all_drivers()
        if not drivers:
            await message.answer("No drivers found!")
            return

        random_driver = random.choice(drivers)
        await state.update_data(current_driver=random_driver)

        await message.answer(
            f"Id: {random_driver['id']}\nDriver: {random_driver['first_name']} {random_driver['last_name']}\nBirth date: {random_driver['birth_day']}\n"
            + f"Address: {random_driver['address']}\nEmail/Phone: This information will be visible once the driver accepts your request!\nMiles dialy: {random_driver['miles_dialy']}\n"
            + f"Miles weekly: {random_driver['miles_weekly']}\n Work days: {random_driver['work_days']}\nHome days: {random_driver['home_days']}",
            reply_markup=create_company_keyboard(random_driver["id"], message.from_user.id),
        )
    except Exception as e:
        print(e)
        await message.answer(
            "Something went wrong, /start - and try again :)",
            reply_markup=types.ReplyKeyboardRemove(),
        )

@router.callback_query(DriverCallback.filter())
async def handle_driver_callback(callback_query: types.CallbackQuery, callback_data: DriverCallback, state: FSMContext):
    try:

        action = callback_data.action
        driver_id = callback_data.driver_id
        requested_company_id = callback_data.requested_company_id

        if action == "cancel":
            await callback_query.message.edit_text("Cancelled 🚫")
            return

        elif action == "next":
            drivers = await get_all_drivers()
            if not drivers:
                await callback_query.answer("No drivers found!")
                return

            random_driver = random.choice(drivers)
            await state.update_data(current_driver=random_driver)

            await callback_query.message.edit_text(
                f"Id: {random_driver['id']}\nDriver: {random_driver['first_name']} {random_driver['last_name']}\nBirth date: {random_driver['birth_day']}\n"
                + f"Address: {random_driver['address']}\nEmail/Phone: This information will be visible once the driver accepts your request!\nMiles dialy: {random_driver['miles_dialy']}\n"
                + f"Miles weekly: {random_driver['miles_weekly']}\n Work days: {random_driver['work_days']}\nHome days: {random_driver['home_days']}",
                reply_markup=create_company_keyboard(random_driver["id"], callback_query.message.chat.id),
            )
            return

        elif action == "send":
            driver = await get_by_id(driver_id, "drivers")
            company = await get_by_id(requested_company_id, "companies")

            # Driverga xabar yuborish
            driver_message = (
                f"New request⚡️\n"+
                f"Company id: {company['id']}\n"+
                f"Name: {company['company_name']}\n"+
                f"DOT: {company['dot']}\n"+
                f"MC: {company['mc']}\n"+
                f"Address: {company['address']}\n"+
                f"Trucks: {company['current_trucks']}\n"+
                f"Email: {company['company_email']}\n"+
                f"Contact: {company['company_contact']}"
            )

            accept_button = InlineKeyboardButton(text="Accept ✅", callback_data=f"accept_{requested_company_id}")
            reject_button = InlineKeyboardButton(text="Reject ❌", callback_data=f"reject_{requested_company_id}")
            reply_markup = InlineKeyboardMarkup(inline_keyboard=[[accept_button, reject_button]])

            await callback_query.bot.send_message(chat_id=driver["id"], text=driver_message, reply_markup=reply_markup)
            await callback_query.answer("Request sent to the driver!")
            return
    except Exception as ex:
        print(ex)
        await callback_query.answer("Slow!")
    
@router.callback_query(lambda c: c.data.startswith("accept_") or c.data.startswith("reject_"))
async def handle_driver_response(callback_query: types.CallbackQuery):
    data = callback_query.data.split("_")
    action = data[0]
    company_id = int(data[1])

    if action == "accept":
        driver = await get_by_id(callback_query.message.chat.id, 'drivers')

        company_message = (f"Driver accepted💥\nId: {driver['id']}\nDriver: {driver['first_name']} {driver['last_name']}\nBirth date: {driver['birth_day']}\n"
            + f"Address: {driver['address']}\nEmail: {driver['email']}\nPhone number: {driver['phone_number']}\nMiles dialy: {driver['miles_dialy']}\n"
            + f"Miles weekly: {driver['miles_weekly']}\n Work days: {driver['work_days']}\nHome days: {driver['home_days']}")
        await callback_query.bot.send_message(chat_id=company_id, text=company_message, reply_markup=create_telegram_user_keyboard(callback_query.message.chat.id, driver['phone_number']))
        await callback_query.answer("Accepted ✅")
        await callback_query.message.edit_text("Accepted ✅")
    elif action == "reject":
        await callback_query.bot.send_message(chat_id=company_id, text=f"Driver: {callback_query.message.chat.id} rejected❌")
        await callback_query.answer("Rejected ❌")
        await callback_query.message.edit_text("Rejected ❌")

