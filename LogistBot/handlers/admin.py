from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from db import *
from .functions import *
import keyboars


router = Router()

@router.message(F.text == "/admin" or F.text == "/panel")
async def openAdminPanel(message: types.Message):
    try:
        user_id = message.from_user.id
        if user_id in config.ADMINS:
            await message.answer("Welcome...", reply_markup=keyboars.admin_menu)
    except Exception as ex:
        print(ex)

@router.message(F.text == "Statistics📊")
async def get_Stat(message: types.Message):
    try:
        if await checkAdmin(message.from_user.id):
            companies_count = await get_rows_count("companies")
            drivers_count = await get_rows_count("drivers")

            await message.answer(f"🚀Companies count: {companies_count}\n🚀Drivers Count: {drivers_count}")
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

    
#region Add company 
class AddCompany(StatesGroup):
    id = State()
    company_name = State()
    dot = State()
    mc = State()
    address = State()
    current_trucks = State()
    company_email = State()
    company_contact = State()

@router.message(F.text == "Add company➕")
async def startAddCompany(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if await checkAdmin(user_id):
            await state.set_state(AddCompany.id)
            await message.answer("Enter telegram id: ", reply_markup=keyboars.cancel)
    except Exception as ex:
        print(ex)

@router.message(AddCompany.id)
async def ask_CompanName(message: types.Message, state: FSMContext):
    try:
        await state.update_data(id=int(message.text))
        await state.set_state(AddCompany.company_name)
        await message.answer("Enter company name: ")
    except:
        await message.answer("Something went wrong, \nCancelling...", reply_markup=keyboars.admin_menu) 

@router.message(AddCompany.company_name)
async def ask_dot(message: types.Message, state: FSMContext):
    try:
        await state.update_data(company_name=message.text)
        await state.set_state(AddCompany.dot)
        await message.answer("Enter DOT: ")
    except:
        await message.answer("Something went wrong, \nCancelling...", reply_markup=keyboars.admin_menu) 

@router.message(AddCompany.dot)
async def ask_mc(message: types.Message, state: FSMContext):
    try:
        await state.update_data(dot=message.text)
        await state.set_state(AddCompany.mc)
        await message.answer("Enter MC: ")
    except:
        await message.answer("Something went wrong, \nCancelling...", reply_markup=keyboars.admin_menu) 

@router.message(AddCompany.mc)
async def ask_address(message: types.Message, state: FSMContext):
    try:
        await state.update_data(mc=message.text)
        await state.set_state(AddCompany.address)
        await message.answer("Enter address: ")
    except:
        await message.answer("Something went wrong, \nCancelling...", reply_markup=keyboars.admin_menu) 

@router.message(AddCompany.address)
async def ask_trucks(message: types.Message, state: FSMContext):
    try:
        await state.update_data(address=message.text)
        await state.set_state(AddCompany.current_trucks)
        await message.answer("Enter current trucks: ")
    except:
        await message.answer("Something went wrong, \nCancelling...", reply_markup=keyboars.admin_menu) 

@router.message(AddCompany.current_trucks)
async def ask_email(message: types.Message, state: FSMContext):
    try:
        await state.update_data(current_trucks=int(message.text))
        await state.set_state(AddCompany.company_email)
        await message.answer("Enter email: ")
    except:
        await message.answer("Something went wrong, \nCancelling...", reply_markup=keyboars.admin_menu) 

@router.message(AddCompany.company_email)
async def ask_contact(message: types.Message, state: FSMContext):
    try:
        await state.update_data(company_email=message.text)
        await state.set_state(AddCompany.company_contact)
        await message.answer("Enter company contact: ")
    except:
        await message.answer("Something went wrong, \nCancelling...", reply_markup=keyboars.admin_menu) 

@router.message(AddCompany.company_contact)
async def finish_addCompany(message: types.Message, state: FSMContext):
    try:
        await state.update_data(company_contact=message.text)
        data = await state.get_data()
        await save_carrier_data(data)
        await state.clear()
        await message.answer("Saved!: ", reply_markup=keyboars.admin_menu)
    except Exception as ex:
        print(ex)
        await message.answer("Something went wrong, \nCancelling...", reply_markup=keyboars.admin_menu) 

#endregion

#region Add driver 
class AddDriver(StatesGroup):
    id = State()
    DriverType = State()
    FirstName = State()
    LastName = State()
    BirthDay = State()
    Address = State()
    Email = State()
    PhoneNumber = State()

@router.message(F.text == "Add driver➕")
async def start_addDriver(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if await checkAdmin(user_id):
            await state.set_state(AddDriver.id)
            await message.answer("Enter driver ID: ", reply_markup=keyboars.cancel)
    except Exception as ex:
        print(ex)

@router.message(AddDriver.id)
async def ask_driverType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(id=int(message.text))
        await state.set_state(AddDriver.DriverType)
        await message.answer("Enter driver type: ", reply_markup=keyboars.driver_types)
    except:
        await message.answer("Invalid ID. Cancelling...", reply_markup=keyboars.admin_menu)

@router.message(AddDriver.DriverType)
async def ask_firstName(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DriverType=message.text)
        await state.set_state(AddDriver.FirstName)
        await message.answer("Enter driver's first name: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong. Cancelling...", reply_markup=keyboars.admin_menu)

@router.message(AddDriver.FirstName)
async def ask_lastName(message: types.Message, state: FSMContext):
    try:
        await state.update_data(FirstName=message.text)
        await state.set_state(AddDriver.LastName)
        await message.answer("Enter driver's last name: ")
    except:
        await message.answer("Something went wrong. Cancelling...", reply_markup=keyboars.admin_menu)

@router.message(AddDriver.LastName)
async def ask_birthDay(message: types.Message, state: FSMContext):
    try:
        await state.update_data(LastName=message.text)
        await state.set_state(AddDriver.BirthDay)
        await message.answer("Enter driver's birthday (YYYY-MM-DD): ")
    except:
        await message.answer("Something went wrong. Cancelling...", reply_markup=keyboars.admin_menu)

@router.message(AddDriver.BirthDay)
async def ask_address(message: types.Message, state: FSMContext):
    try:
        await state.update_data(BirthDay=message.text)
        await state.set_state(AddDriver.Address)
        await message.answer("Enter driver's address: ")
    except:
        await message.answer("Invalid date format. Cancelling...", reply_markup=keyboars.admin_menu)

@router.message(AddDriver.Address)
async def ask_email(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Address=message.text)
        await state.set_state(AddDriver.Email)
        await message.answer("Enter driver's email: ")
    except:
        await message.answer("Something went wrong. Cancelling...", reply_markup=keyboars.admin_menu)

@router.message(AddDriver.Email)
async def ask_phoneNumber(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Email=message.text)
        await state.set_state(AddDriver.PhoneNumber)
        await message.answer("Enter driver's phone number: ")
    except:
        await message.answer("Something went wrong. Cancelling...", reply_markup=keyboars.admin_menu)

@router.message(AddDriver.PhoneNumber)
async def finish_addDriver(message: types.Message, state: FSMContext):
    try:
        await state.update_data(PhoneNumber=message.text)
        data = await state.get_data()
        await save_driver(data)  # Ma'lumotlarni saqlash funksiyasi
        await state.clear()
        await message.answer("Driver information saved!", reply_markup=keyboars.admin_menu)
    except Exception as ex:
        print(ex)
        await message.answer("Something went wrong. Cancelling...", reply_markup=keyboars.admin_menu)

#endregion

#region Search company
class SearchCompany(StatesGroup):
    Search = State()

@router.message(F.text == "Search company🔎")
async def searchCompany(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if await checkAdmin(user_id):
            await state.set_state(SearchCompany.Search)
            await message.answer("Enter company id or name: ", reply_markup=keyboars.cancel)
    except Exception as ex:
        print(ex)

@router.message(SearchCompany.Search)
async def finishSearchCompany(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Search=message.text)
        data = await state.get_data()
        await state.clear()
        foundedCompanies = await search_company(data['Search'])
        if len(foundedCompanies) == 0:
            await message.answer("Company not found!", reply_markup=keyboars.admin_menu)
            return
        for company in foundedCompanies:
            await message.answer(f"ID: {company['id']}\nCompany name: {company['company_name']}\nDOT: {company['dot']}\nMC: {company['mc']}\nAddress: {company['address']}\nTrucks: {company['current_trucks']}\nEmail: {company['company_email']}\nContact: {company['company_contact']}", reply_markup=keyboars.admin_menu)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

#endregion

#region Search driver
class SearchDriver(StatesGroup):
    Search = State()

@router.message(F.text == "Search driver🔎")
async def searchCompany(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if await checkAdmin(user_id):
            await state.set_state(SearchDriver.Search)
            await message.answer("Enter driver id or name: ", reply_markup=keyboars.cancel)
    except Exception as ex:
        print(ex)

@router.message(SearchDriver.Search)
async def finishSearchCompany(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Search=message.text)
        data = await state.get_data()
        await state.clear()
        foundDrivers = await search_driver(data['Search'])
        if len(foundDrivers) == 0:
            await message.answer("Driver not found!", reply_markup=keyboars.admin_menu)
            return

        for driver in foundDrivers:
            driverInfo = f"""
Id: {driver['id']}
Driver type: {driver['driver_type']}
First name: {driver['first_name']}
Last name: {driver['last_name']}
Birth date: {driver['birth_day']}
Address: {driver['address']}
Email: {driver['email']}
Phone: {driver['phone_number']}"""

        await message.answer(driverInfo)

    
    except Exception as ex:
        print(ex)
        await message.answer("Something went wrong, please try again, /start - and try again")


#endregion


#region Delete company by id
class CompanyDelete(StatesGroup):
    Id = State()

@router.message(F.text == "Delete company❌")
async def handleCompanyDelete(message: types.Message, state: FSMContext):
    try:
        await state.set_state(CompanyDelete.Id)
        await message.answer("Enter company id:", reply_markup=cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDelete.Id)
async def deleteCompany(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Id=int(message.text))
        data = await state.get_data()
        await state.clear()
        company = await get_by_id(data["Id"], "companies")
        if not company:
            await message.answer("Company not found with this id!", reply_markup=keyboars.admin_menu)
            return
        
        await delete_by_id(data["Id"], "companies")
        await message.answer("Deleted!", reply_markup=keyboars.admin_menu)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")


class DriverDelete(StatesGroup):
    Id = State()

@router.message(F.text == "Delete driver❌")
async def handleDriverDelete(message: types.Message, state: FSMContext):
    try:
        await state.set_state(DriverDelete.Id)
        await message.answer("Enter driver id:", reply_markup=cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(DriverDelete.Id)
async def deleteDriver(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Id=int(message.text))
        data = await state.get_data()
        await state.clear()
        driver = await get_by_id(data["Id"], "drivers")
        if not driver:
            await message.answer("Driver not found with this id!", reply_markup=keyboars.admin_menu)
            return
        
        await delete_by_id(data["Id"], "drivers")
        await message.answer("Deleted!", reply_markup=keyboars.admin_menu)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")
