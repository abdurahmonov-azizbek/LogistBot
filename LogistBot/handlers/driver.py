from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, StatesGroupMeta
from aiogram.types import file, reply_keyboard_markup
from db import *
import keyboars
from bot_instance import bot, dp
import os
from aiogram.types import *
from .functions import *
import uuid
from handlers.base import checkBalance

router = Router()


# region Driver registration
class DriverRegistration(StatesGroup):
    DriverType = State()
    FirstName = State()
    LastName = State()
    BirthDay = State()
    Address = State()
    Email = State()
    PhoneNumber = State()


@router.message(F.text == "Driver")
async def ask_driver_type_for_registration(message: types.Message, state: FSMContext):
    try:
        
        await state.set_state(DriverRegistration.DriverType)
        await message.answer("[1/7] Choose driver type: ", reply_markup=keyboars.driver_types)
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())


@router.message(DriverRegistration.DriverType)
async def ask_FirstName(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DriverType=message.text)
        await state.set_state(DriverRegistration.FirstName)
        await message.answer("[2/7] Enter first name: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())


@router.message(DriverRegistration.FirstName)
async def ask_lastName(message: types.Message, state: FSMContext):
    try:
        await state.update_data(FirstName=message.text)
        await state.set_state(DriverRegistration.LastName)
        await message.answer("[3/7] Enter last name: ")
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())


@router.message(DriverRegistration.LastName)
async def ask_birthDay(message: types.Message, state: FSMContext):
    try:
        await state.update_data(LastName=message.text)
        await state.set_state(DriverRegistration.BirthDay)
        await message.answer("[4/7] Enter your birth date: ")
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())


@router.message(DriverRegistration.BirthDay)
async def ask_Address(message: types.Message, state: FSMContext):
    try:
        await state.update_data(BirthDay=message.text)
        await state.set_state(DriverRegistration.Address)
        await message.answer("[5/7] Enter your address: ")
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())


@router.message(DriverRegistration.Address)
async def ask_email(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Address=message.text)
        await state.set_state(DriverRegistration.Email)
        await message.answer("[6/7] Enter your email: ")
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())


@router.message(DriverRegistration.Email)
async def ask_phone(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Email=message.text)
        await state.set_state(DriverRegistration.PhoneNumber)
        await message.answer("[7/7] Enter your phone number: ")
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())


@router.message(DriverRegistration.PhoneNumber)
async def finish_driver_registration(message: types.Message, state: FSMContext):
    try:
        # formatting us phone number
        phone_number = message.text
        phone_number = phone_number.replace(" ", "").replace("\t", "").replace("\n", "")
        if not phone_number.startswith("+1"):
            phone_number = "+1" + phone_number.lstrip("1")

        await state.update_data(PhoneNumber=phone_number)
        data = await state.get_data()
        data.update({'id': message.from_user.id})
        await save_driver(data)
        await save_driver_status(message.from_user.id, True)
        await save_driver_balance(message.from_user.id, 0)
        await state.clear()
        await message.answer("Amazing!, Thank you", reply_markup=keyboars.driver_main_menu)
    except:
        await message.answer("Something went wrong, /start - and try again :)",
                             reply_markup=types.ReplyKeyboardRemove())


# endregion

# region Company driver more info filling
class CompanyDriverMoreInfo(StatesGroup):
    MilesDialy = State()
    MilesWeekly = State()
    WorkDaysType = State()
    WorkDays = State()
    HomeDays = State()
    NightOrDayTimePU = State()


@router.message(F.text == "More info (only for Company drivers)")
async def start_CompanyDriverFilling(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        driver = await get_by_id(user_id, "drivers")

        if not driver:
            await message.answer("You are not driver!")
            return

        if driver['driver_type'] != "Company driver":
            await message.answer("This part is for only company drivers!")
            return

        if driver['miles_dialy'] != None:
            await message.answer("You have already filled it)")
            return

        await state.set_state(CompanyDriverMoreInfo.MilesDialy)
        await message.answer("[1/6] Enter miles dialy: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CompanyDriverMoreInfo.MilesDialy)
async def ask_milesWeekly(message: types.Message, state: FSMContext):
    try:
        await state.update_data(MilesDialy=message.text)
        await state.set_state(CompanyDriverMoreInfo.MilesWeekly)
        await message.answer("[2/6] Enter miles weekly: ")
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CompanyDriverMoreInfo.MilesWeekly)
async def ask_WorkDaysType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(MilesWeekly=message.text)
        await state.set_state(CompanyDriverMoreInfo.WorkDaysType)
        await message.answer("[3/6] Enter type for Work days: ", reply_markup=keyboars.weeks_months)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CompanyDriverMoreInfo.WorkDaysType)
async def ask_WorkDays(message: types.Message, state: FSMContext):
    try:
        await state.update_data(WorkDaysType=message.text)
        await state.set_state(CompanyDriverMoreInfo.WorkDays)
        await message.answer("[4/6] Enter work days: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CompanyDriverMoreInfo.WorkDays)
async def ask_homeDays(message: types.Message, state: FSMContext):
    try:
        await state.update_data(WorkDays=message.text)
        await state.set_state(CompanyDriverMoreInfo.HomeDays)
        await message.answer("[5/6] Enter home days: ")
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CompanyDriverMoreInfo.HomeDays)
async def ask_NightOrDayTimePU(message: types.Message, state: FSMContext):
    try:
        await state.update_data(HomeDays=message.text)
        await state.set_state(CompanyDriverMoreInfo.NightOrDayTimePU)
        await message.answer("[6/6] Enter nighr or day time PU: ", reply_markup=keyboars.yes_no_skip)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CompanyDriverMoreInfo.NightOrDayTimePU)
async def finish_CompanyDriverMoreInfo(message: types.Message, state: FSMContext):
    try:
        await state.update_data(NightOrDayTimePU=message.text)
        data = await state.get_data()
        data.update({'id': message.from_user.id})
        await save_company_driver_more_info(data)
        await state.clear()
        await message.answer("Good!, Keep using...", reply_markup=keyboars.driver_main_menu)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


# endregion

# region Filling CDL information
class CDL(StatesGroup):
    Cdl = State()
    StateOfCdl = State()
    Class = State()
    ExpireDate = State()
    IssueDate = State()


@router.message(F.text == "CDL")
async def start_cdl(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        driver = await get_by_id(user_id, "drivers")
        if not driver:
            await message.answer("You are not driver!")
            return

        cdl = await get_by_id(user_id, "cdls")
        if cdl:
            await message.answer("You have already filled it", reply_markup=keyboars.driver_main_menu)
            return

        await state.set_state(CDL.Cdl)
        await message.answer("[1/5] Enter your cdl: ", reply_markup=keyboars.cancel)

    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CDL.Cdl)
async def ask_state(message: types.Message, state: FSMContext):
    try:
        await state.update_data(Cdl=message.text)
        await state.set_state(CDL.StateOfCdl)
        await message.answer("[2/5] Enter state of CDL: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CDL.StateOfCdl)
async def ask_class(message: types.Message, state: FSMContext):
    try:
        await state.update_data(StateOfCdl=message.text)
        await state.set_state(CDL.Class)
        await message.answer("[3/5] Select your class? ", reply_markup=keyboars.driver_cdl_classes)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CDL.Class)
async def ask_expireDate(message: types.Message, state: FSMContext):
    try:
        text = message.text
        if text.lower() not in "abcd":
            await message.answer("You should use buttons for answer!")
            return

        await state.update_data(Class=text)
        await state.set_state(CDL.ExpireDate)
        await message.answer("[4/5] Enter expire date, [month/day/year]: ", reply_markup=keyboars.cancel)

    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CDL.ExpireDate)
async def ask_issueDate(message: types.Message, state: FSMContext):
    try:
        await state.update_data(ExpireDate=message.text)
        await state.set_state(CDL.IssueDate)
        await message.answer("[5/5] Enter issue date, [month/day/year]: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(CDL.IssueDate)
async def finish_cdl(message: types.Message, state: FSMContext):
    try:
        await state.update_data(IssueDate=message.text)
        data = await state.get_data()
        data.update({'id': message.from_user.id})
        await save_cdl(data=data)
        await state.clear()
        await message.answer("Amazing, Keep using )", reply_markup=keyboars.driver_main_menu)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


# endregion

# region Medical Card information

class MedicalCard(StatesGroup):
    NationalRegistry = State()
    ExpirationDate = State()
    DateCertificateSigned = State()


@router.message(F.text == "Medical Card")
async def start_MedicalCardFilling(message: types.Message, state: FSMContext):
    try:
        driver = await get_by_id(message.from_user.id, "drivers")
        if not driver:
            await message.answer("You must be driver!")
            return

        medicalCard = await get_by_id(message.from_user.id, "MedicalCards")

        if medicalCard:
            await message.answer("You have already filled it)")
            return

        await state.set_state(MedicalCard.NationalRegistry)
        await message.answer("[1/3] Enter your national registry: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(MedicalCard.NationalRegistry)
async def ask_expirationdate(message: types.Message, state: FSMContext):
    try:
        await state.update_data(NationalRegistry=message.text)
        await state.set_state(MedicalCard.ExpirationDate)
        await message.answer("[2/3] Enter expiration date: ")
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(MedicalCard.ExpirationDate)
async def ask_datecertified(message: types.Message, state: FSMContext):
    try:
        await state.update_data(ExpirationDate=message.text)
        await state.set_state(MedicalCard.DateCertificateSigned)
        await message.answer("[3/3] Enter date certificate signed: ")
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(MedicalCard.DateCertificateSigned)
async def finish_medicalCardInformation(message: types.Message, state: FSMContext):
    try:
        await state.update_data(DateCertificateSigned=message.text)
        data = await state.get_data()
        data.update({'id': message.from_user.id})
        await save_medical_card(data=data)
        await state.clear()
        await message.answer("Amazing, Keep using )", reply_markup=keyboars.driver_main_menu)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


class Note(StatesGroup):
    Note = State()

@router.message(F.text == "Note")
async def ask_note(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        driver = await get_by_id(user_id, "drivers")
        if not driver:
            await message.answer("You must be driver!")
            return
        
        note = await get_by_id(user_id, "DriverNotes")
        if note:
            await message.answer("You have already filled it.")
            return

        await state.set_state(Note.Note)
        await message.answer("Enter your note: ", reply_markup=keyboars.cancel)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


@router.message(Note.Note)
async def finish_note(message: types.Message, state: FSMContext):
    try:
        if not isinstance(message.text, str):
            await message.answer("Invalid input. Please enter text only.")
            return

        note = message.text
        if len(note) > 1000 or len(note) < 10:
            await message.answer("Note length must be between 10 and 1000!")
            return

        # Save the note
        await state.update_data(note=note)
        data = await state.get_data()
        data.update({'id': message.from_user.id})
        await save_driver_note(data=data)
        await state.clear()
        await message.answer("Amazing! Your note has been saved.", reply_markup=keyboars.driver_main_menu)
    except Exception as ex:
        print(f"Error: {ex}")
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())


#region CDL image upload
# CDL image upload functions
MAX_FILE_SIZE = 4 * 1024 * 1024  # 4 MB

class CDLStates(StatesGroup):
    FirstImage = State()
    SecondImage = State()

@dp.message(F.text == "Upload CDL")
async def startCdlUpload(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        driver = await get_by_id(user_id, "drivers")
        if not driver:
            return
        await create_cdl_folder(user_id)
        await state.set_state(CDLStates.FirstImage)
        await message.answer(f"Send me the front side of your cdl image", reply_markup=keyboars.cancel)

    except Exception as ex:
        print(ex)
        await message.answer("Something wrong, Please try again.")

@dp.message(CDLStates.FirstImage, F.photo | F.document)
async def handle_first_image(message: Message, state: FSMContext):
    try:
        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.document and message.document.mime_type.startswith("image"):
            if message.document.file_size > MAX_FILE_SIZE:
                await message.answer("The file size is 4 MB and should be used.")
                return
            file_id = message.document.file_id
        else:
            await message.answer("Please send only image!")
            return
    
        await state.update_data(first=file_id)
        await state.set_state(CDLStates.SecondImage)
        await message.answer("Now, send me the Back side of your cdl")
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())
    
@dp.message(CDLStates.SecondImage, F.photo | F.document)
async def handle_second_image(message: Message, state: FSMContext):
    try:
        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.document and message.document.mime_type.startswith("image"):
            if message.document.file_size > MAX_FILE_SIZE:
                await message.answer("The file size is 4 MB and should be used.")
                return
            file_id = message.document.file_id
        else:
            await message.answer("Please send only image!")
            return
    
        await message.answer("Uploading....")
        await state.update_data(second=file_id)
        data = await state.get_data()
        await state.clear()

        firstFile = await bot.get_file(data['first'])
        secondFile = await bot.get_file(data['second'])
        first_file_name = str(uuid.uuid4()) + ".jpg"
        second_file_name = str(uuid.uuid4()) + ".jpg"
        cdl_path = os.path.join(os.curdir, "images", "cdl", str(message.from_user.id))
        await bot.download_file(firstFile.file_path, os.path.join(cdl_path, first_file_name))
        await bot.download_file(secondFile.file_path, os.path.join(cdl_path, second_file_name))
        save_information = {
            'id': message.from_user.id,
            'front_side': os.path.join(cdl_path, first_file_name),
            'back_side': os.path.join(cdl_path, second_file_name)
        }
        await save_cdl_image(save_information)
        await message.answer("Saved, Thank you!", reply_markup=keyboars.driver_main_menu)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())
#endregion

#region Change last uploaded cdl images
class ChangeCDLStates(StatesGroup):
    FrontSide = State()
    BackSide = State()

@router.message(F.text == "Change CDL")
async def changeLastCdl(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        last_cdl = await get_latest_by_date(user_id, "cdl_image", "created_date")
        if not last_cdl:
            await message.answer("You need to upload CDL image first, before change it!")
            return

        front_side = FSInputFile(last_cdl['front_side'])
        back_side = FSInputFile(last_cdl['back_side'])
        media = [
            InputMediaPhoto(media=front_side),
            InputMediaPhoto(media=back_side, caption="Your current CDL image"),
        ]
        await bot.send_media_group(user_id, media=media)
        await message.answer("If you want to change it, please send the front side of your new cdl image", reply_markup=keyboars.cancel)
        await state.set_state(ChangeCDLStates.FrontSide)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(ChangeCDLStates.FrontSide, F.photo | F.document)
async def change_frontside(message: types.Message, state: FSMContext):
    try:
        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.document and message.document.mime_type.startswith("image"):
            if message.document.file_size > MAX_FILE_SIZE:
                await message.answer("The file size is 4 MB and should be used.")
                return
            file_id = message.document.file_id
        else:
            await message.answer("Please send only image!")
            return

        await state.update_data(first=file_id)
        await message.answer("Ok. now send back side")
        await state.set_state(ChangeCDLStates.BackSide)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(ChangeCDLStates.BackSide, F.photo | F.document)
async def change_frontside(message: types.Message, state: FSMContext):
    try:
        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.document and message.document.mime_type.startswith("image"):
            if message.document.file_size > MAX_FILE_SIZE:
                await message.answer("The file size is 4 MB and should be used.")
                return
            file_id = message.document.file_id
        else:
            await message.answer("Please send only image!")
            return

        await state.update_data(second=file_id)
        data = await state.get_data()
        await state.clear()
        await message.answer("Changing....")

        user_id = message.from_user.id
        last_cdl = await get_latest_by_date(user_id, "cdl_image", "created_date")
        if not last_cdl:
            return
        
        delete_result = await delete_by_id(last_cdl['unique_id'], "cdl_image", "unique_id")
        print(delete_result)

        firstFile = await bot.get_file(data['first'])
        secondFile = await bot.get_file(data['second'])
        first_file_name = str(uuid.uuid4()) + ".jpg"
        second_file_name = str(uuid.uuid4()) + ".jpg"
        cdl_path = os.path.join(os.curdir, "images", "cdl", str(user_id))
        await bot.download_file(firstFile.file_path, os.path.join(cdl_path, first_file_name))
        await bot.download_file(secondFile.file_path, os.path.join(cdl_path, second_file_name))
        save_information = {
            'id': user_id,
            'front_side': os.path.join(cdl_path, first_file_name),
            'back_side': os.path.join(cdl_path, second_file_name)
        }
        await save_cdl_image(save_information)

        os.remove(last_cdl['front_side'])
        os.remove(last_cdl['back_side'])

        await message.answer("Done✅", reply_markup=keyboars.driver_main_menu)
    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())

#endregion

#startregion Upload Medical Card image
class MedicalCardImageStates(StatesGroup):
    Image = State()

@router.message(F.text == "Upload Medical Card")
async def start_upload_medcard(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        old_medical_card = await get_by_id(user_id, "medical_card_image")
        if old_medical_card:
            await message.answer("You already upload medical card!")
            return
        
        await create_medical_card_folder(user_id)
        await state.set_state(MedicalCardImageStates.Image)
        await message.answer("Ok, send medical card image", reply_markup=keyboars.cancel)

    except:
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(MedicalCardImageStates.Image, F.photo | F.document)
async def save_medicalcard(message: types.Message, state: FSMContext):
    try:
        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.document and message.document.mime_type.startswith("image"):
            if message.document.file_size > MAX_FILE_SIZE:
                await message.answer("The file size is 4 MB and should be used.")
                return
            file_id = message.document.file_id
        else:
            await message.answer("Please send only image!")
            return

        await state.update_data(image=file_id)
        data = await state.get_data()
        await state.clear()

        await message.answer("Uploading...")
        user_id = message.from_user.id
        image = await bot.get_file(data['image'])
        medical_card_path = os.path.join(os.curdir, "images", "medicalcard", str(user_id))
        image_name = str(uuid.uuid4()) + ".jpg"
        await bot.download_file(image.file_path, os.path.join(medical_card_path, image_name))
        save_info = {
            'id': user_id,
            'file_path': os.path.join(medical_card_path, image_name)
        }

        await save_medical_card_image(save_info)
        await message.answer("Saved✅", reply_markup=keyboars.driver_main_menu)
    except Exception as e:
        print(e)
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())

#endregion
#region Change Medical card
class ChangeMedicalCardStates(StatesGroup):
    Image = State()

@router.message(F.text == "Change Medical Card")
async def start_change_medcard_image(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        old_medcard = await get_by_id(user_id, "medical_card_image")
        if not old_medcard:
            await message.answer("You must be uploaded medical card before change it!")
            return 

        image = FSInputFile(old_medcard['file_path'])
        await state.set_state(ChangeMedicalCardStates.Image)
        await bot.send_photo(user_id, photo=image, caption="Your current medical card image!")
        await message.answer("If you want to change it, send new medical card image", reply_markup=keyboars.cancel)
        await state.set_state(ChangeMedicalCardStates.Image)

    except Exception as e:
        print(e)
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())

@router.message(ChangeMedicalCardStates.Image, F.photo | F.document)
async def changeMedCardImage(message: types.Message, state: FSMContext):
    try:
        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.document and message.document.mime_type.startswith("image"):
            if message.document.file_size > MAX_FILE_SIZE:
                await message.answer("The file size is 4 MB and should be used.")
                return
            file_id = message.document.file_id
        else:
            await message.answer("Please send only image!")
            return

        await state.update_data(image=file_id)
        data = await state.get_data()
        await state.clear()
        await message.answer("Changing...")
        user_id = message.from_user.id
        
        old_medcard = await get_by_id(user_id, "medical_card_image")
        if not old_medcard:
            os.remove(old_medcard['file_path'])
        await delete_by_id(user_id, "medical_card_image")
        image = await bot.get_file(data['image'])
        medical_card_path = os.path.join(os.curdir, "images", "medicalcard", str(user_id))
        image_name = str(uuid.uuid4()) + ".jpg"
        image_path = os.path.join(medical_card_path, image_name)
        await bot.download_file(image.file_path, image_path)
        save_info = {
            'id': user_id,
            'file_path': image_path
        }
        await save_medical_card_image(save_info)
        
        await message.answer("Done✅", reply_markup=keyboars.driver_main_menu)

    except Exception as e:
        print(e)
        await message.answer("Something went wrong, /start - try again", reply_markup=types.ReplyKeyboardRemove())