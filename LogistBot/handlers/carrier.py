from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.filters import Command
from .functions import *
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from db import *
import keyboars
from bot_instance import bot

router = Router()

class CarrierRegistration(StatesGroup):
    CompanyName = State()
    DOT = State()
    MC = State()
    Address = State()
    CurrentTrucks = State()
    CompanyEmail = State()
    CompanyContact = State()

# region Carrier registration
@router.message(F.text == "Carrier")
async def start_carrier_registration(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    company = await get_by_id(user_id, "companies")
    
    if company:
        await message.answer("It seems you're already registered. Use the main menu to manage your account.", reply_markup=keyboars.carrier_main_menu)
        return

    await state.set_state(CarrierRegistration.CompanyName)
    await message.answer("[1/7] Enter company name !", reply_markup=keyboars.cancel)

#Kompaniya nomi
@router.message(CarrierRegistration.CompanyName)
async def ask_dot(message: types.Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    await state.set_state(CarrierRegistration.DOT)
    await message.answer("[2/7] Enter your DOT number:", reply_markup=keyboars.cancel)

# DOT raqami
@router.message(CarrierRegistration.DOT)
async def ask_mc(message: types.Message, state: FSMContext):
    await state.update_data(dot=message.text)
    await state.set_state(CarrierRegistration.MC)
    await message.answer("[3/7] Enter your MC number:", reply_markup=keyboars.cancel)

# MC raqami
@router.message(CarrierRegistration.MC)
async def ask_address(message: types.Message, state: FSMContext):
    await state.update_data(mc=message.text)
    await state.set_state(CarrierRegistration.Address)
    await message.answer("[4/7] Enter company mail address ? (Example: Address, City, State, ZIP) ", reply_markup=keyboars.cancel)

# Manzil
@router.message(CarrierRegistration.Address)
async def ask_current_trucks(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(CarrierRegistration.CurrentTrucks)
    await message.answer("[5/7] How many company trucks you have (number of trucks) ?", reply_markup=keyboars.cancel)

# Yuk mashinalari soni
@router.message(CarrierRegistration.CurrentTrucks)
async def ask_email(message: types.Message, state: FSMContext):
    trucks_number = message.text

    if not trucks_number.isdigit():
        await message.answer("Please enter a valid number for trucks.")
        return

    await state.update_data(current_trucks=int(trucks_number))
    await state.set_state(CarrierRegistration.CompanyEmail)
    await message.answer("[6/7] Enter company contact email address!", reply_markup=keyboars.cancel)

# Email
@router.message(CarrierRegistration.CompanyEmail)
async def ask_contact(message: types.Message, state: FSMContext):
    await state.update_data(company_email=message.text)
    await state.set_state(CarrierRegistration.CompanyContact)
    await message.answer("[7/7] Enter company contact number!", reply_markup=keyboars.cancel)

# Kontakt va ma'lumotlarni saqlash
@router.message(CarrierRegistration.CompanyContact)
async def finish_registration(message: types.Message, state: FSMContext):
    # formatting us phone number
    phone_number = message.text
    phone_number = phone_number.replace(" ", "").replace("\t", "").replace("\n", "")
    if not phone_number.startswith("+1"):
        phone_number = "+1" + phone_number.lstrip("1")

    await state.update_data(company_contact=phone_number)
    data = await state.get_data()
    data.update({"id": message.from_user.id})
    await save_carrier_data(data)  # Ma'lumotlarni saqlash
    await save_company_balance(message.from_user.id, 100) # Yangi company uchun balance yaratish
    await save_default_driver_filter(message.from_user.id)

    # taklif qilingan yoki yo'qligini tekshirish
    user_id = message.from_user.id
    referal = await get_by_id(user_id, "referals", "invited_user_id")
    settings = await get_settings()
    if referal:
        reffer_id = referal['id']
        reffer = await get_by_id(reffer_id, "companies")
        if reffer:
            balance = await get_by_id(reffer_id, "CompanyBalance")
            await update_balance("CompanyBalance", reffer_id, balance['balance'] + settings['referal_price_for_company'])
            
        else:
            reffer = await get_by_id(reffer_id, "drivers")
            balance = await get_by_id(reffer_id, "DriverBalance")
            await update_balance("DriverBalance", reffer_id, balance['balance'] + settings['referal_price_for_company'])

        await delete_by_id(message.from_user.id, "referals", "invited_user_id")
        try:
            await bot.send_message(reffer_id, "🎉 Congratulations, the reward has been added to your account")
        except:
            pass
            

    await state.clear()
    await message.answer("Amazing! \nRegistration complete!", reply_markup=keyboars.carrier_main_menu)


#region Filling special load offer
class CarrierSpecialLoads(StatesGroup):
    Amazon = State()
    PO_LOADS = State()
    DRY_VAN = State()
    Line_Loads = State()

@router.message(F.text == "Driver Load Offer Details")
async def start_filling_special_load_offer(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    company = await get_by_id(user_id, "companies")
    if not company:
        print("[!] Company bolib royhatdan otmasdan turib bu malumotni toldirib bolmaydi!")
        return
    
    old_data = await get_by_id(user_id, "SpecialLoads")
    if old_data:
        await message.answer("You have already filled.")
        return 

    await state.set_state(CarrierSpecialLoads.Amazon)
    await message.answer("[1/4] Are you hauling amazon loads ? ", reply_markup=keyboars.yes_no_skip)

@router.message(CarrierSpecialLoads.Amazon)
async def ask_po_loads(message: types.Message, state: FSMContext):
    if message.text not in ["YES", "NO", "SKIP"]:
        await message.answer("You should use YES/NO/SKIP for answer!")
        return

    await state.update_data(amazon=message.text)
    await state.set_state(CarrierSpecialLoads.PO_LOADS)
    await message.answer("[2/4] Power only (PO) ? ")

@router.message(CarrierSpecialLoads.PO_LOADS)
async def ask_dry_van(message: types.Message, state: FSMContext):
    if message.text not in ["YES", "NO", "SKIP"]:
        await message.answer("You should use YES/NO/SKIP for answer!")
        return
    
    await state.update_data(po_loads = message.text)
    await state.set_state(CarrierSpecialLoads.DRY_VAN)
    await message.answer("[3/4] DRY VAN? ")

@router.message(CarrierSpecialLoads.DRY_VAN)
async def ask_line_loads(message: types.Message, state: FSMContext):
    await state.update_data(dry_van=message.text)
    await state.set_state(CarrierSpecialLoads.Line_Loads)
    await message.answer("[4/4] Do you have dedicated lanes ? ")

@router.message(CarrierSpecialLoads.Line_Loads)
async def finish_special_loads(message: types.Message, state: FSMContext):
    await state.update_data(line_loads=message.text)
    data = await state.get_data()
    data.update({"id": message.from_user.id})
    await save_special_loads(data)
    await state.clear()
    await message.answer("Amazing, Thank you!", reply_markup=keyboars.carrier_main_menu)
#endregion

#region Filling Company driver offer
class CompanyDriverOffers(StatesGroup):
    DriverSalaryForSoloUsd = State()
    DriverSalaryForSoloPercentage = State()
    DriverSalaryForTeamUsd = State()
    EscrowPerWeek = State()
    EscrowTotal = State()
    Layover = State()
    AvaiableTruckNumbers = State()
    AvaiableTrucksMake = State()
    TruckSpeed = State()
    MinimumExperienceRequirement = State()

@router.message(F.text == "Offer for company driver")
async def start_filling_company_driver_offer(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        company = await get_by_id(user_id, "companies")

        if company is None:
            await message.answer("You must be registered as a company first!")
            return
        
        driver_offer = await get_by_id(user_id, "CompanyDriverOffers")
        if driver_offer:
            await message.answer("You have already filled it :)")
            return
        
        
        await state.set_state(CompanyDriverOffers.DriverSalaryForSoloUsd)
        await message.answer("[1/10] Solo driver pay $ ? (Example: 0.60 or 0.70) ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.DriverSalaryForSoloUsd)
async def ask_amount_of_driver_salary_forSolor(message: types.Message, state: FSMContext):
    try:          
        await state.update_data(DriverSalaryForSoloUsd=message.text)
        await state.set_state(CompanyDriverOffers.DriverSalaryForSoloPercentage)
        await message.answer("[2/10] Enter driver salary for solo (%) ?  ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.DriverSalaryForSoloPercentage)
async def ask_type_for_driverSalaryForTeam(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DriverSalaryForSoloPercentage=message.text)
        await state.set_state(CompanyDriverOffers.DriverSalaryForTeamUsd)
        await message.answer("[3/10] TEAM drivers pay  $ ? (Example: 0.75 or 0.90) ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.DriverSalaryForTeamUsd)
async def ask_escrow_per_week(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DriverSalaryForTeamUsd=message.text)
        await state.set_state(CompanyDriverOffers.EscrowPerWeek)
        await message.answer("[4/10] Escrow per week? ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.EscrowPerWeek)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(EscrowPerWeek=message.text)
        await state.set_state(CompanyDriverOffers.EscrowTotal)
        await message.answer("[5/10] Escrow total? ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")


@router.message(CompanyDriverOffers.EscrowTotal)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(EscrowTotal=message.text)
        await state.set_state(CompanyDriverOffers.Layover)
        await message.answer("[6/10] Layover fee $ (daily)", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.Layover)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:

        await state.update_data(Layover=message.text)
        await state.set_state(CompanyDriverOffers.AvaiableTruckNumbers)
        await message.answer("[7/10] Available trucks ? (Example: 11) ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.AvaiableTruckNumbers)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(AvaiableTruckNumbers=message.text)
        await state.set_state(CompanyDriverOffers.AvaiableTrucksMake)
        await message.answer("[8/10] Enter year average of available trucks ? (Example: 2020 - 2024)", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")


@router.message(CompanyDriverOffers.AvaiableTrucksMake)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(AvaiableTrucksMake=message.text)
        await state.set_state(CompanyDriverOffers.TruckSpeed)
        await message.answer("[9/10] Speed governor ? (Example: 65Mph or 75Mph)", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")


@router.message(CompanyDriverOffers.TruckSpeed)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(TruckSpeed=message.text)
        await state.set_state(CompanyDriverOffers.MinimumExperienceRequirement)
        await message.answer("[10/10] Min. Driver experience requirement ? (3 month or 2 years)", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")


@router.message(CompanyDriverOffers.MinimumExperienceRequirement)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(MinimumExperienceRequirement=message.text)
        data = await state.get_data()
        data.update({'id': message.from_user.id})
        await save_company_driver_offer(data)
        await state.clear()
        await message.answer("Amazing! Thank you.", reply_markup=keyboars.carrier_main_menu)
    except Exception as ex:
        print(ex)
        await message.answer("Something went wrong, please try again, /start - and try again")
#endregion

#region Owner driver info
class OwnerDriverOffers(StatesGroup):
    DispatchService = State()
    OfficeAdmin = State()
    Ifta = State()
    Insurance = State()

@router.message(F.text == "Offer for owner driver")
async def start_owner_driver_offer(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    company = await get_by_id(user_id, "companies")

    if not company:
        await message.answer("You are not company!")
        return

    owner_driver = await get_by_id(user_id, "OwnerDriverOffers")
    if owner_driver:
        await message.answer("You have already filled it")
        return

    await state.set_state(OwnerDriverOffers.DispatchService)
    await message.answer("[1/4] Company fees (weekly) ?", reply_markup=keyboars.cancel)

@router.message(OwnerDriverOffers.DispatchService)
async def ask_OfficeAdminType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DispatchService = message.text)
        await state.set_state(OwnerDriverOffers.OfficeAdmin)
        await message.answer("[2/4] Admin fee (weekly) ?", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - and try again.")

@router.message(OwnerDriverOffers.OfficeAdmin)
async def ask_ifta(message: types.Message, state: FSMContext):
    try:
        await state.update_data(OfficeAdmin=message.text)
        await state.set_state(OwnerDriverOffers.Ifta)
        await message.answer("[3/4] IFTA (weekly) ?", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - and try again.")

@router.message(OwnerDriverOffers.Ifta)
async def ask_insurance(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Ifta=message.text)
        await state.set_state(OwnerDriverOffers.Insurance)
        await message.answer("[4/4] Insurance fee (weekly) ?", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - and try again.")

@router.message(OwnerDriverOffers.Insurance)
async def finish_ownerDriverOfferFilling(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Insurance=message.text)
        data = await state.get_data()
        data.update({'id': message.from_user.id})
        await save_owner_driver_offer(data)
        await state.clear()
        await message.answer("Amazing, keep using :)", reply_markup=keyboars.carrier_main_menu)
    except:
        await message.answer("Something went wrong, /start - and try again.")
#endregion

#region Offer for lease driver
class LeaseDriverOffers(StatesGroup):
    TruckRentalFee = State()
    TruckMiles = State()
    DispatchService = State()
    OfficeAdminUsd = State()
    Ifta = State()
    InsuranceType = State()
    Insurance = State()

@router.message(F.text == "Offer for lease driver")
async def start_leaseDriverOffers(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        company = await  get_by_id(user_id, "companies")
        if not company:
            await message.answer("You are not company!, You can't fill informations!")
            return

        lease_driver_offer = await  get_by_id(user_id, "LeaseDriverOffers")
        if lease_driver_offer:
            await message.answer("You have already filled it :)")
            return

        await state.set_state(LeaseDriverOffers.TruckRentalFee)
        await message.answer("[1/7] Weekly truck rent fee $ ?", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.TruckRentalFee)
async def ask_truckMiles(message: types.Message, state: FSMContext):
    try:
        await state.update_data(TruckRentalFee=message.text)
        await state.set_state(LeaseDriverOffers.TruckMiles)
        await message.answer("[2/7] Per mile fee ? (Example: 0.13 per miles or 0.15 per miles) ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.TruckMiles)
async def ask_dispatchService(message: types.Message, state: FSMContext):
    try:
        await state.update_data(TruckMiles=message.text)
        await state.set_state(LeaseDriverOffers.DispatchService)
        await message.answer("[3/7] Company fees (weekly) ?")
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.DispatchService)
async def ask_safetyServiceType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DispatchService=message.text)
        await state.set_state(LeaseDriverOffers.OfficeAdminUsd)
        await message.answer("[4/7] Admin fee (weekly) ?", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again )")


@router.message(LeaseDriverOffers.OfficeAdminUsd)
async def ask_ifta(message: types.Message, state: FSMContext):
    try:
        await state.update_data(OfficeAdminUsd=message.text)
        await state.set_state(LeaseDriverOffers.Ifta)
        await message.answer("[5/7] IFTA (weekly) ?")
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.Ifta)
async def ask_insuranceType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Ifta=message.text)
        await state.set_state(LeaseDriverOffers.InsuranceType)
        await message.answer("[6/7] Select insurance type: ", reply_markup=keyboars.per_week_month)
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.InsuranceType)
async def ask_Insurance(message: types.Message, state: FSMContext):
    try:
        await state.update_data(InsuranceType=message.text)
        await state.set_state(LeaseDriverOffers.Insurance)
        await message.answer("[7/7] Enter insurance: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.Insurance)
async def finish_leaseDriverOffer(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Insurance=message.text)
        data = await state.get_data()
        data.update({'id': message.from_user.id})
        await save_lease_driver_offer(data)
        await state.clear()
        await message.answer("Amazing, thank you!", reply_markup=keyboars.carrier_main_menu)
    except:
        await message.answer("Something went wrong, /start - try again )")

#endregion

