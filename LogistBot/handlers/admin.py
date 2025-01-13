from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db import *
from .functions import *
import keyboars
from config import ADMINS
from bot_instance import bot
import asyncio
from db import *

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

#endregion
#region Add Money Company

class AddMoneyCompany(StatesGroup):
    Amount = State()

@router.message(F.text == "Add money COMPANY")
async def startAddMoneyCompany(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            await state.set_state(AddMoneyCompany.Amount)
            await message.answer("Enter amount: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(AddMoneyCompany.Amount)
async def addMoneyToCompany(message: types.Message, state: FSMContext):
    try:
        amount = str(message.text)
        if not amount.isdigit():
            await message.answer("Enter only numbers!")
            return
        
        await state.update_data(amount=int(amount))
        data = await state.get_data()
        amount = data['amount']
        await state.clear()
        await message.answer("Proccecing....")
        companies_balance = await get_all("CompanyBalance")
        
        for company_balance in companies_balance:
            await update_balance("CompanyBalance", company_balance['id'], company_balance['balance'] + amount)

        await message.answer("Done!", reply_markup=admin_menu)

    except:
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

#region

#region Add money DRIVER
class AddMoneyDriver(StatesGroup):
    Amount = State()

@router.message(F.text == "Add money DRIVER")
async def startAddMoneyDriver(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            await state.set_state(AddMoneyDriver.Amount)
            await message.answer("Enter amount: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(AddMoneyDriver.Amount)
async def addMoneyToDriver(message: types.Message, state: FSMContext):
    try:
        amount = str(message.text)
        if not amount.isdigit():
            await message.answer("Enter only numbers!")
            return
        
        await state.update_data(amount=int(amount))
        data = await state.get_data()
        amount = data['amount']
        await state.clear()
        await message.answer("Proccecing....")
        drivers_balance = await get_all("DriverBalance")
        
        for driver_balance in drivers_balance:
            await update_balance("DriverBalance", driver_balance['id'], driver_balance['balance'] + amount)

        await message.answer("Done!", reply_markup=admin_menu)

    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())


#endregion

#region Send message to all companies
class SendMessageCompany(StatesGroup):
    Message = State()

@router.message(F.text == "Send message to companies")
async def sendMessageCompanies(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            await state.set_state(SendMessageCompany.Message)
            await message.answer("Enter message to send to all companies: ", reply_markup=keyboars.cancel)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(SendMessageCompany.Message)
async def sendToAllCompanies(message: types.Message, state: FSMContext):
    try:
        content = message.text
        companies = await get_all("companies")
        await message.answer("Sending....")
        errs = 0
        for company in companies:
            try:
                bot.send_message(company['id'], content)
                await asyncio.sleep(0.5)
            except:
                errs += 1
                continue
        await message.answer(f"Done, errors: {errs}, Sent: {len(companies)-errs}", reply_markup=admin_menu)
        
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())
#endregion

#region Send message to all drivers
class SendMessageDriver(StatesGroup):
    Message = State()

@router.message(F.text == "Send message to drivers")
async def sendMessageDrivers(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            await state.set_state(SendMessageDriver.Message)
            await message.answer("Enter message to send to all drivers: ", reply_markup=keyboars.cancel)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(SendMessageDriver.Message)
async def sendToAllDrivers(message: types.Message, state: FSMContext):
    try:
        content = message.text
        drivers = await get_all("drivers")
        await message.answer("Sending...")
        errs = 0
        for driver in drivers:
            try:
                bot.send_message(driver['id'], content)
                await asyncio.sleep(0.5)
            except:
                errs += 1
                continue
        await message.answer(f"Done, Error: {errs} Sent: {len(drivers)-errs}", reply_markup=admin_menu)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())
#endregion

#region Add one company balance
class AddOneCompanyBalanceStates(StatesGroup):
    Id = State()
    Amount = State()

@router.message(F.text == "Add money to one company balance")
async def startAddMoneyToOneCompanyBalance(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            await state.set_state(AddOneCompanyBalanceStates.Id)
            await message.answer("Enter company id: ", reply_markup=keyboars.cancel)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(AddOneCompanyBalanceStates.Id)
async def ask_Amount(message: types.Message, state: FSMContext):
    try:
        company_id = int(message.text)
        await state.update_data(id=company_id)
        await state.set_state(AddOneCompanyBalanceStates.Amount)
        await message.answer("Enter amount: ")
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(AddOneCompanyBalanceStates.Amount)
async def addMoneyToOneCompanyBalance(message: types.Message, state: FSMContext):
    try:
        await state.update_data(amount=int(message.text))
        data = await state.get_data()
        await state.clear()
        company_id = data['id']
        amount = data['amount']
        company_balance = await get_by_id(company_id, "CompanyBalance")
        await update_balance("CompanyBalance", company_id, company_balance['balance'] + amount)
        await message.answer("Added!", reply_markup=keyboars.admin_menu)

    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

#endregion

#region Add money to one driver's balance
class AddOneDriverBalanceStates(StatesGroup):
    Id = State()
    Amount = State()

@router.message(F.text == "Add money to one driver balance")
async def startAddMoneyToOneDriverBalance(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            await state.set_state(AddOneDriverBalanceStates.Id)
            await message.answer("Enter driver id: ", reply_markup=keyboars.cancel)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(AddOneDriverBalanceStates.Id)
async def ask_Amount(message: types.Message, state: FSMContext):
    try:
        driver_id = int(message.text)
        await state.update_data(id=driver_id)
        await state.set_state(AddOneDriverBalanceStates.Amount)
        await message.answer("Enter amount: ")
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(AddOneDriverBalanceStates.Amount)
async def addMoneyToOneDriverBalance(message: types.Message, state: FSMContext):
    try:
        await state.update_data(amount=int(message.text))
        data = await state.get_data()
        await state.clear()
        driver_id = data['id']
        amount = data['amount']
        driver_balance = await get_by_id(driver_id, "DriverBalance")
        await update_balance("DriverBalance", driver_id, driver_balance['balance'] + amount)
        await message.answer("Added!", reply_markup=keyboars.admin_menu)

    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())
#endregion

#region Set invite link price for company
class SetRefPriceCompany(StatesGroup):
    Amount = State()

@router.message(F.text == "Set invite price for company")
async def setCompanyRefPrice(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            await state.set_state(SetRefPriceCompany.Amount)
            await message.answer("Enter amount: ", reply_markup=keyboars.cancel)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(SetRefPriceCompany.Amount)
async def setRefPriceForCompany(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        await state.clear()
        await update_settings("referal_price_for_company", amount)
        await message.answer("Updated!", reply_markup=keyboars.admin_menu)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

#endregion

#region Set invite link price for driver
class SetRefPriceDriver(StatesGroup):
    Amount = State()

@router.message(F.text == "Set invite price for driver")
async def setDriverRefPrice(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            await state.set_state(SetRefPriceDriver.Amount)
            await message.answer("Enter amount: ", reply_markup=keyboars.cancel)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(SetRefPriceDriver.Amount)
async def setRefPriceForDriver(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        await state.clear()
        await update_settings("referal_price_for_driver", amount)
        await message.answer("Updated!", reply_markup=keyboars.admin_menu)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())
#endregion

#region Set price for company
class PriceForCompany(StatesGroup):
    Amount = State()

@router.message(F.text == "Set price for company")
async def handleSetPriceForCompany(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            await state.set_state(PriceForCompany.Amount)
            await message.answer("Enter amount: ", reply_markup=keyboars.cancel)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(PriceForCompany.Amount)
async def updatePriceForCompany(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        await state.clear()
        await update_settings("daily_price_for_company", amount)
        await message.answer("Updated!", reply_markup=keyboars.admin_menu)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

#endregion

#region Set price for driver
class PriceForDriver(StatesGroup):
    Amount = State()

@router.message(F.text == "Set price for driver")
async def handleSetPriceForDriver(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            await state.set_state(PriceForDriver.Amount)
            await message.answer("Enter amount: ", reply_markup=keyboars.cancel)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(PriceForDriver.Amount)
async def updatePriceForDriver(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        await state.clear()
        await update_settings("daily_price_for_driver", amount)
        await message.answer("Updated!", reply_markup=keyboars.admin_menu)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())

#endregion
@router.message(F.text == "Show prices⚙️")
async def showPrices(message: types.Message):
    try:
        user_id = message.from_user.id
        if user_id in ADMINS:
            settings = await get_settings()
            await message.answer(f"🏢Dialy price for company: {settings['daily_price_for_company']}$\n🚚Dialy price for driver: {settings['daily_price_for_driver']}$\n🖇Invite price for company: {settings['referal_price_for_company']}$\n🖇Invite price for driver: {settings['referal_price_for_driver']}$")
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, please try again, /start - and try again", reply_markup=types.ReplyKeyboardRemove())