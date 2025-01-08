from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from db import *
from .functions import *
import keyboars
import asyncio
from config import ADMINS

router = Router()

#region Show Account
@router.message(F.text == "Account")
async def show_account(message: types.Message):
    # try to get company
    try:
        message.reply("wait...")
        user_id = message.from_user.id
        company = await get_by_id(user_id, "companies")
        if company:
            company_informations = await get_company_full_info(company=company, user_id=user_id)
            for info in company_informations:
                await message.answer(info)
                await asyncio.sleep(1)

            return
        
        driver = await get_by_id(user_id, "drivers")
        if driver:
            driver_information = await get_driver_full_info(driver, user_id)
            for driver_info in driver_information:
                await message.answer(driver_info)
                await asyncio.sleep(1)
                
            return
    except:
        await message.answer("Something went wrong, sorry.")
#endregion

# Qo'shimcha malumotlarni qabul qilib olish
@router.message(F.text == "Add Informationℹ️")
async def show_options(message: types.Message):
    await message.answer("Wait...")
    user_id = message.from_user.id
    company = await get_by_id(user_id, "companies")
    if company:
        company_info_menu = []
        special_load_offered = await get_by_id(user_id, "SpecialLoads")
        if not special_load_offered:
            company_info_menu.append([KeyboardButton(text="Driver Load Offer Details")])

        offer_for_company_driver = await get_by_id(user_id, "CompanyDriverOffers")
        if not offer_for_company_driver:
            company_info_menu.append([KeyboardButton(text="Offer for company driver")])

        offer_for_owner_driver = await get_by_id(user_id, "OwnerDriverOffers")
        if not offer_for_owner_driver:
            company_info_menu.append([KeyboardButton(text="Offer for owner driver")])

        offer_for_lease_driver = await get_by_id(user_id, "LeaseDriverOffers")
        if not offer_for_lease_driver:
            company_info_menu.append([KeyboardButton(text="Offer for lease driver")])

        if len(company_info_menu) == 0:
            await message.answer("You have filled all information.")
            return 
        
        company_info_menu.append([KeyboardButton(text="◀️Back to Main Menu")])

        
        await message.answer("Please select an option for fill: ", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=company_info_menu))
        return
    
    driver = await get_by_id(user_id, "drivers")
    if driver:
        driver_info_menu = []
        if driver['driver_type'] == "Company driver" and (driver['miles_dialy'] == None and driver['nigth_or_day_time_PU'] == None):
            driver_info_menu.append([KeyboardButton(text="More info (only for Company drivers)")])

        cdl = await get_by_id(user_id, "cdls")
        if not cdl:
            driver_info_menu.append([KeyboardButton(text="CDL")])

        medical_card = await get_by_id(user_id, "MedicalCards")
        if not medical_card:
            driver_info_menu.append([KeyboardButton(text="Medical Card")])

        note = await get_by_id(user_id, "DriverNotes")
        if not note:
            driver_info_menu.append([KeyboardButton(text="Note")])

        if len(driver_info_menu) == 0:
            await message.answer("You have filled all information.")
            return 
        

        driver_info_menu.append([KeyboardButton(text="CDL (image)")])

        driver_info_menu.append([KeyboardButton(text="◀️Back to Main Menu")])


        await message.answer("Please select an option for fill: ", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=driver_info_menu))
        return

# Back to main menu handler )
@router.message(F.text == "◀️Back to Main Menu")
async def go_back_menu(message: types.Message):
    company = await get_by_id(message.from_user.id, "companies")
    if company:
        await message.answer("Your role: Carrier\nWelcome...", reply_markup=keyboars.carrier_main_menu)
        return
    
    driver = await get_by_id(message.from_user.id, "drivers")
    if driver:
        await message.answer("Your role: Driver\nWelcome...", reply_markup=keyboars.driver_main_menu)
        return
    
    await message.answer("Menu🔽", reply_markup=keyboars.register_keyboard)
    # keyingi role larda ham handle qilish kerak )

class EditState(StatesGroup):
    TableName = State()
    Column = State()
    NewValue = State()

@router.message(F.text == "Edit✏️")
async def handle_edit(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        company = await get_by_id(user_id, "companies")
        if company:
            company_tables_keyboars = []
            for value in keyboars.company_tables.values():
                company_tables_keyboars.append([KeyboardButton(text=value)])

            company_tables_keyboars.append([KeyboardButton(text="Cancel⬅️")])

            await state.set_state(EditState.TableName)
            await message.answer("Select table you want to change info:", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=company_tables_keyboars))

        driver = await get_by_id(user_id, "drivers")
        if driver:
            driver_tables_keyboard = []
            for value in keyboars.driver_tables.values():
                driver_tables_keyboard.append([KeyboardButton(text=value)])
            
            driver_tables_keyboard.append([KeyboardButton(text="Cancel⬅️")])
            await state.set_state(EditState.TableName)
            await message.answer("Select table you want to change info:", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=driver_tables_keyboard))

    except:
        await message.answer("Something went wrong, /start - try again )", reply_markup=keyboars.cancel)


@router.message(EditState.TableName)
async def ask_Column(message: types.Message, state: FSMContext):
    try:
        table = message.text
        if table not in keyboars.company_tables.values() and table not in keyboars.driver_tables.values():
            await message.answer("Use buttons!")
            return

        company = await get_by_id(message.from_user.id, "companies")        
        if company:
            for key, value in keyboars.company_tables.items():
                if value == message.text:
                    table = key
        else:
            for key, value in keyboars.driver_tables.items():
                if value == message.text:
                    table = key

        if key == "":
            await message.answer("Invalid input. Please use buttons!")
            return
        
        await state.update_data(TableName=table)
    
        columns_keyboard = []
        if table == "companies":
            for key, value in keyboars.companies_columns.items():
                columns_keyboard.append([KeyboardButton(text=value)])
        elif table == "CompanyDriverOffers":
            for value in keyboars.CompanyDriverOffers_columns.values():
                columns_keyboard.append([KeyboardButton(text=value)])
        elif table == "SpecialLoads":
            for value in keyboars.SpecialLoads_columns.values():
                columns_keyboard.append([KeyboardButton(text=value)])
        elif table == "LeaseDriverOffers":
            for value in keyboars.LeaseDriverOffers_columns.values():
                columns_keyboard.append([KeyboardButton(text=value)])
        elif table == "OwnerDriverOffers":
            for value in keyboars.OwnerDriverOffers_columns.values():
                columns_keyboard.append([KeyboardButton(text=value)])  
        elif table == "drivers":
            driver = await get_by_id(message.from_user.id, "drivers")
            if driver['driver_type'] == 'Company driver':
                for key, value in keyboars.drivers_columns.items():
                    columns_keyboard.append([KeyboardButton(text=value)])
            else:
                for key, value in keyboars.drivers_columns.items():
                    if key not in ["miles_dialy", "miles_weekly", "work_days_type", "work_days", "home_days", "nigth_or_day_time_PU"]:
                        columns_keyboard.append([KeyboardButton(text=value)]) 
        
        elif table == "cdls":
            for value in keyboars.cdls_columns.values():
                columns_keyboard.append([KeyboardButton(text=value)])    
        elif table == "MedicalCards":
            for value in keyboars.MedicalCards_columns.values():
                columns_keyboard.append([KeyboardButton(text=value)])    

        if table == "drivers":
            driver = await get_by_id(message.from_user.id, "drivers")
            if driver['driver_type'] != 'Company driver':
                columns_keyboard.remove

        columns_keyboard.append([KeyboardButton(text="Cancel⬅️")])
        await state.set_state(EditState.Column)
        await message.answer("Select column for update", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=columns_keyboard))
    except:
        await message.answer("Something went wrong, /start - try again )", reply_markup=keyboars.cancel)


@router.message(EditState.Column)
async def ask_NewValue(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        user_id = message.from_user.id
        table = data['TableName']
        column = message.text

        if table == "companies":
            for key, value in keyboars.companies_columns.items():
                if value == column:
                    column = key
                    break
        elif table == "CompanyDriverOffers":
            for key, value in keyboars.CompanyDriverOffers_columns.items():
                if value == column:
                    column = key
                    break
        elif table == "SpecialLoads":
            for key, value in keyboars.SpecialLoads_columns.items():
                if value == column:
                    column = key
                    break
        elif table == "LeaseDriverOffers":
            for key, value in keyboars.LeaseDriverOffers_columns.items():
                if value == column:
                    column = key
                    break
        elif table == "OwnerDriverOffers":
            for key, value in keyboars.OwnerDriverOffers_columns.items():
                if value == column:
                    column = key
                    break
        elif table == "drivers":
            for key, value in keyboars.drivers_columns.items():
                if value == column:
                    column = key
                    break
        elif table == "cdls":
            for key, value in keyboars.cdls_columns.items():
                if value == column:
                    column = key
                    break
        elif table == "MedicalCards":
            for key, value in keyboars.MedicalCards_columns.items():
                if value == column:
                    column = key
                    break


        old_value = await  get_one_column(table, column, user_id)
        # if old_value is None:
        #     await message.answer(f"You must be entered it before!", keyboars.cancel)
            
        await state.update_data(Column=column)
        await state.set_state(EditState.NewValue)
        await message.answer(f"Current value is: {old_value}, \nIf you want to change it please enter: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again )", reply_markup=keyboars.cancel)


@router.message(EditState.NewValue)
async def checkAndUpdateColumn(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        await state.update_data(NewValue=message.text)
        data = await state.get_data()
        await state.clear()

        await update_one_column(user_id, data['TableName'], data['Column'], data['NewValue'])
        await message.answer(f"Saved!", reply_markup=await GetMainMenu(user_id))
    except:
        await message.answer("Something wrong, Please try again.")


