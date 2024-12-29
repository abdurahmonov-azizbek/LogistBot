from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.filters import Command
from .functions import *
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from db import *
import keyboars

router = Router()

class CarrierRegistration(StatesGroup):
    CompanyName = State()
    DOT = State()
    MC = State()
    Address = State()
    CurrentTrucks = State()
    CompanyEmail = State()
    CompanyContact = State()

class CarrierSpecialLoads(StatesGroup):
    Amazon = State()
    PO_LOADS = State()
    DRY_VAN = State()
    Broker_Loads = State()
    Line_Loads = State()

class CompanyDriverOffers(StatesGroup):
    DriverSalaryForSoloType = State()
    DriverSalaryForSolo = State()
    DriverSalaryForTeamType = State()
    DriverSalaryForTeam = State()
    EscrowPerWeek = State()
    EscrowTotal = State()
    Layover = State()
    DetensionForEachExtraStop = State()
    AvaiableTruckNumbers = State()
    AvaiableTrucksMake = State()
    TruckSpeed = State()
    MinimumExperienceRequirement = State()

class OwnerDriverOffers(StatesGroup):
    DispatchService = State()
    SafetyServiceType = State()
    SafetyService = State()
    # OfficeAdminType = State()
    OfficeAdmin = State()
    Ifta = State()
    InsuranceType = State()
    Insurance = State()

class LeaseDriverOffers(StatesGroup):
    TruckRentalFeeType = State()
    TruckRentalFee = State()
    TruckMiles = State()
    DispatchService = State()
    SafetyServiceType = State()
    SafetyService = State()
    # OfficeAdminType = State()
    OfficeAdmin = State()
    Ifta = State()
    InsuranceType = State()
    Insurance = State()

# region Carrier registration
@router.message(F.text == "Carrier")
async def start_carrier_registration(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    company = await get_by_id(user_id, "companies")
    
    if company:
        await message.answer("It seems you're already registered. Use the main menu to manage your account.", reply_markup=keyboars.carrier_main_menu)
        return

    await state.set_state(CarrierRegistration.CompanyName)
    await message.answer("[1/7] Enter the name of your company: ", reply_markup=keyboars.cancel)

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
    await message.answer("[4/7] Enter your address (e.g., Address, City, State, ZIP Code):", reply_markup=keyboars.cancel)

# Manzil
@router.message(CarrierRegistration.Address)
async def ask_current_trucks(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(CarrierRegistration.CurrentTrucks)
    await message.answer("[5/7] Enter the total number of company trucks", reply_markup=keyboars.cancel)

# Yuk mashinalari soni
@router.message(CarrierRegistration.CurrentTrucks)
async def ask_email(message: types.Message, state: FSMContext):
    trucks_number = message.text

    if not trucks_number.isdigit():
        await message.answer("Please enter a valid number for trucks.")
        return

    await state.update_data(current_trucks=int(trucks_number))
    await state.set_state(CarrierRegistration.CompanyEmail)
    await message.answer("[6/7] Enter your company email:", reply_markup=keyboars.cancel)

# Email
@router.message(CarrierRegistration.CompanyEmail)
async def ask_contact(message: types.Message, state: FSMContext):
    await state.update_data(company_email=message.text)
    await state.set_state(CarrierRegistration.CompanyContact)
    await message.answer("[7/7] Enter your company contact number:", reply_markup=keyboars.cancel)

# Kontakt va ma'lumotlarni saqlash
@router.message(CarrierRegistration.CompanyContact)
async def finish_registration(message: types.Message, state: FSMContext):
    await state.update_data(company_contact=message.text, tg_user_id=message.from_user.id)
    data = await state.get_data()
    data.update({"id": message.from_user.id})
    await save_carrier_data(data)  # Ma'lumotlarni saqlash
    await save_default_driver_filter(message.from_user.id)
    await state.clear()
    await message.answer("Amazing! \nRegistration complete!", reply_markup=keyboars.carrier_main_menu)


#region Filling special load offer

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
    await message.answer("Please use these options for answer!\n[1/5] Are there any Amazon loads currently available for drivers? ", reply_markup=keyboars.yes_no_skip)

@router.message(CarrierSpecialLoads.Amazon)
async def ask_po_loads(message: types.Message, state: FSMContext):
    if message.text not in ["YES", "NO", "SKIP"]:
        await message.answer("You should use YES/NO/SKIP for answer!")
        return

    await state.update_data(amazon=message.text)
    await state.set_state(CarrierSpecialLoads.PO_LOADS)
    await message.answer("[2/5] Are there any Power-only (PO) loads currently available for drivers? ")

@router.message(CarrierSpecialLoads.PO_LOADS)
async def ask_dry_van(message: types.Message, state: FSMContext):
    if message.text not in ["YES", "NO", "SKIP"]:
        await message.answer("You should use YES/NO/SKIP for answer!")
        return
    
    await state.update_data(po_loads = message.text)
    await state.set_state(CarrierSpecialLoads.DRY_VAN)
    await message.answer("[3/5] DRY VAN? ")

@router.message(CarrierSpecialLoads.DRY_VAN)
async def ask_broker_leads(message: types.Message, state: FSMContext):
    await state.update_data(dry_van=message.text)
    await state.set_state(CarrierSpecialLoads.Broker_Loads)
    await message.answer("[4/5] Broker Leads ?")

@router.message(CarrierSpecialLoads.Broker_Loads)
async def ask_line_loads(message: types.Message, state: FSMContext):
    await state.update_data(broker_loads=message.text)
    await state.set_state(CarrierSpecialLoads.Line_Loads)
    await message.answer("[5/5] Are there any current Line loads available for drivers? ")

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
        
        
        await state.set_state(CompanyDriverOffers.DriverSalaryForSoloType)
        # await message.answer("[1/12] Enter type for driver salary for solo? ", reply_markup=keyboars.dollar_percentage)
        await message.answer("[1/12] Enter driver salary for solo ($) ? ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.DriverSalaryForSoloType)
async def ask_amount_of_driver_salary_forSolor(message: types.Message, state: FSMContext):
    try:  
        # if message.text not in ["$", "%"]:
        #     await message.answer("Wrong type!, Please try again.")
        #     return
        
        await state.update_data(DriverSalaryForSoloType=message.text)
        await state.set_state(CompanyDriverOffers.DriverSalaryForSolo)
        await message.answer("[2/12] Enter driver salary for solo (%) ?  ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.DriverSalaryForSolo)
async def ask_type_for_driverSalaryForTeam(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DriverSalaryForSolo=message.text)
        await state.set_state(CompanyDriverOffers.DriverSalaryForTeamType)
        await message.answer("[3/12] Enter driver salary for team ($) ? ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.DriverSalaryForTeamType)
async def ask_amount_of_driverSalaryForTeam(message: types.Message, state: FSMContext):
    try:
        # if message.text not in ["$", "%"]:
        #     await message.answer("Wrong type, Please try again.")
        #     return 
        
        await state.update_data(DriverSalaryForTeamType=message.text)
        await state.set_state(CompanyDriverOffers.DriverSalaryForTeam)
        await message.answer("[4/12] Enter driver salary for team (%): ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")


@router.message(CompanyDriverOffers.DriverSalaryForTeam)
async def ask_escrow_per_week(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DriverSalaryForTeam=message.text)
        await state.set_state(CompanyDriverOffers.EscrowPerWeek)
        await message.answer("[5/12] Escrow per week? ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.EscrowPerWeek)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(EscrowPerWeek=message.text)
        await state.set_state(CompanyDriverOffers.EscrowTotal)
        await message.answer("[6/12] Escrow total? ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")


@router.message(CompanyDriverOffers.EscrowTotal)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(EscrowTotal=message.text)
        await state.set_state(CompanyDriverOffers.Layover)
        await message.answer("[7/12] Enter layover?", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.Layover)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Layover=message.text)
        await state.set_state(CompanyDriverOffers.DetensionForEachExtraStop)
        await message.answer("[8/12] Detension for each extra stop ?", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.DetensionForEachExtraStop)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:

        await state.update_data(DetensionForEachExtraStop=message.text)
        await state.set_state(CompanyDriverOffers.AvaiableTruckNumbers)
        await message.answer("[9/12] Avaiable truck numbers ?", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")

@router.message(CompanyDriverOffers.AvaiableTruckNumbers)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(AvaiableTruckNumbers=message.text)
        await state.set_state(CompanyDriverOffers.AvaiableTrucksMake)
        await message.answer("[10/12] Avaiable Trucks make ?", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")


@router.message(CompanyDriverOffers.AvaiableTrucksMake)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(AvaiableTrucksMake=message.text)
        await state.set_state(CompanyDriverOffers.TruckSpeed)
        await message.answer("[11/12] Truck speed ?", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")


@router.message(CompanyDriverOffers.TruckSpeed)
async def ask_escrow_total(message: types.Message, state: FSMContext):
    try:
        await state.update_data(TruckSpeed=message.text)
        await state.set_state(CompanyDriverOffers.MinimumExperienceRequirement)
        await message.answer("[12/12] Minimum experience requirement ?", reply_markup=keyboars.cancel)
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
    except:
        await message.answer("Something went wrong, please try again, /start - and try again")
#endregion

#region Owner driver info
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
    await message.answer("[1/7] Dispatch service: ", reply_markup=keyboars.cancel)

@router.message(OwnerDriverOffers.DispatchService)
async def ask_SafetyServiceType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DispatchService=message.text)
        await state.set_state(OwnerDriverOffers.SafetyServiceType)
        await message.answer("[2/7] Savety service ($): ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - and try again.")

@router.message(OwnerDriverOffers.SafetyServiceType)
async def ask_SafetyService(message: types.Message, state: FSMContext):
    try:
        await state.update_data(SafetyServiceType=message.text)
        await state.set_state(OwnerDriverOffers.SafetyService)
        await message.answer("[3/7] Safety service (%): ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - and try again.")

@router.message(OwnerDriverOffers.SafetyService)
async def ask_OfficeAdminType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(SafetyService = message.text)
        await state.set_state(OwnerDriverOffers.OfficeAdmin)
        await message.answer("[4/7] Office admin ($): ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - and try again.")

# @router.message(OwnerDriverOffers.OfficeAdminType)
# async def ask_officeAdmin(message: types.Message, state: FSMContext):
#     try:
#         await state.update_data(OfficeAdminType=message.text)
#         await state.set_state(OwnerDriverOffers.OfficeAdmin)
#         await message.answer("[5/8] Office admin (%): ", reply_markup=keyboars.cancel)
#     except:
#         await message.answer("Something went wrong, /start - and try again.")

@router.message(OwnerDriverOffers.OfficeAdmin)
async def ask_ifta(message: types.Message, state: FSMContext):
    try:
        await state.update_data(OfficeAdmin=message.text)
        await state.set_state(OwnerDriverOffers.Ifta)
        await message.answer("[5/7] IFTA: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - and try again.")

@router.message(OwnerDriverOffers.Ifta)
async def ask_insuranceType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Ifta=message.text)
        await state.set_state(OwnerDriverOffers.InsuranceType)
        await message.answer("[6/7] Select insurance type (per week/month)", reply_markup=keyboars.per_week_month)
    except:
        await message.answer("Something went wrong, /start - and try again.")

@router.message(OwnerDriverOffers.InsuranceType)
async def ask_insurance(message: types.Message, state: FSMContext):
    try:
        await state.update_data(InsuranceType=message.text)
        await state.set_state(OwnerDriverOffers.Insurance)
        await message.answer("[7/7] Enter insurance: ", reply_markup=keyboars.cancel)
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

        await state.set_state(LeaseDriverOffers.TruckRentalFeeType)
        await message.answer("[1/10] Select truck rental fee type: ", reply_markup=keyboars.per_week_month)
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.TruckRentalFeeType)
async def ask_truckRentalFee(message: types.Message, state: FSMContext):
    try:
        await state.update_data(TruckRentalFeeType=message.text)
        await state.set_state(LeaseDriverOffers.TruckRentalFee)
        await message.answer("[2/10] Enter truck rental fee: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.TruckRentalFee)
async def ask_truckMiles(message: types.Message, state: FSMContext):
    try:
        await state.update_data(TruckRentalFee=message.text)
        await state.set_state(LeaseDriverOffers.TruckMiles)
        await message.answer("[3/10] Enter truck miles ($1.23 per mile): ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.TruckMiles)
async def ask_dispatchService(message: types.Message, state: FSMContext):
    try:
        await state.update_data(TruckMiles=message.text)
        await state.set_state(LeaseDriverOffers.DispatchService)
        await message.answer("[4/10] Enter dispatch service: ")
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.DispatchService)
async def ask_safetyServiceType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DispatchService=message.text)
        await state.set_state(LeaseDriverOffers.SafetyServiceType)
        await message.answer("[5/10] Select safety service ($): ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.SafetyServiceType)
async def ask_safetyService(message: types.Message, state: FSMContext):
    try:
        await state.update_data(SafetyServiceType=message.text)
        await state.set_state(LeaseDriverOffers.SafetyService)
        await message.answer("[6/10] Enter safety service (%): ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.SafetyService)
async def ask_officeAdminType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(SafetyService=message.text)
        await state.set_state(LeaseDriverOffers.OfficeAdmin)
        await message.answer("[7/10] Select office admin ($): ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again )")

# @router.message(LeaseDriverOffers.OfficeAdminType)
# async def ask_officeAdmin(message: types.Message, state: FSMContext):
#     try:
#         await state.update_data(OfficeAdminType=message.text)
#         await state.set_state(LeaseDriverOffers.OfficeAdmin)
#         await message.answer("[8/11] Enter office admin (%): ",reply_markup=keyboars.cancel)
#     except:
#         await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.OfficeAdmin)
async def ask_ifta(message: types.Message, state: FSMContext):
    try:
        await state.update_data(OfficeAdmin=message.text)
        await state.set_state(LeaseDriverOffers.Ifta)
        await message.answer("[8/10] Enter ifta: ")
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.Ifta)
async def ask_insuranceType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Ifta=message.text)
        await state.set_state(LeaseDriverOffers.InsuranceType)
        await message.answer("[9/10] Select insurance type: ", reply_markup=keyboars.per_week_month)
    except:
        await message.answer("Something went wrong, /start - try again )")

@router.message(LeaseDriverOffers.InsuranceType)
async def ask_Insurance(message: types.Message, state: FSMContext):
    try:
        await state.update_data(InsuranceType=message.text)
        await state.set_state(LeaseDriverOffers.Insurance)
        await message.answer("[10/10] Enter insurance: ", reply_markup=keyboars.cancel)
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

