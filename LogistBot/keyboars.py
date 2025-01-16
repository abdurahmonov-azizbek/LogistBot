from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

register_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Carrier")],
        [KeyboardButton(text="Driver")],
    ],
)

carrier_main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Search Drivers🔍"), KeyboardButton(text="Account")],
        [KeyboardButton(text="Add Informationℹ️"), KeyboardButton(text="Settings⚙️")],
        [KeyboardButton(text="Delete Account❌"), KeyboardButton(text="Edit✏️")],
        [KeyboardButton(text="Invite friends🔗"), KeyboardButton(text="Support🔧")]
    ],
)

carrier_info_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Driver Load Offer Details"),
            KeyboardButton(text="Offer for company driver"),
            KeyboardButton(text="Offer for owner driver"),
            KeyboardButton(text="Offer for lease driver"),
        ],
        [KeyboardButton(text="◀️Back to Main Menu")],
    ],
)

driver_info_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="More info (only for Company drivers)")],
        # [KeyboardButton(text="CDL")],
        # [KeyboardButton(text="Medical Card")],
        [KeyboardButton(text="Note")],
        [KeyboardButton(text="Upload CDL")],
        [KeyboardButton(text="Change CDL")],
        [KeyboardButton(text="Upload Medical Card")],
        [KeyboardButton(text="Change Medical Card")],
        [KeyboardButton(text="◀️Back to Main Menu")],
    ],
)

yes_no_skip = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="YES"),
            KeyboardButton(text="NO"),
            KeyboardButton(text="SKIP"),
        ]
    ],
)

dollar_percentage = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text="$"), KeyboardButton(text="%")]],
)

per_week_month = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text="PER WEEK"), KeyboardButton(text="PER MONTH")]],
)

driver_types = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Company driver")],
        [KeyboardButton(text="Owner driver")],
        [KeyboardButton(text="Lease driver")],
        [KeyboardButton(text="Cancel⬅️")],
    ],
)


cancel = ReplyKeyboardMarkup(
    resize_keyboard=True, keyboard=[[KeyboardButton(text="Cancel⬅️")]]
)

driver_main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Search Companies🔎"), KeyboardButton(text="Account")],
        [KeyboardButton(text="Add Informationℹ️"), KeyboardButton(text="Status⚙️")],
        [KeyboardButton(text="Delete Account❌"), KeyboardButton(text="Edit✏️")],
        [KeyboardButton(text="Invite friends🔗"), KeyboardButton(text="Support🔧")]
    ],
)


yes_no = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text="YES I'M SURE")], [KeyboardButton(text="Cancel⬅️")]],
)

weeks_months = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text="WEEKS"), KeyboardButton(text="MONTHS")]],
)

driver_cdl_classes = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="A"),
            KeyboardButton(text="B"),
            KeyboardButton(text="C"),
            KeyboardButton(text="D"),
        ]
    ],
)

active_passive = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="ACTIVE"), KeyboardButton(text="PASSIVE")],
        [KeyboardButton(text="Cancel⬅️")],
    ],
)

yesno = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="YES"), KeyboardButton(text="NO")],
        [KeyboardButton(text="Cancel⬅️")],
    ],
)

admin_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Statistics📊"), KeyboardButton(text="Show prices⚙️")],
        [KeyboardButton(text="Add company➕"), KeyboardButton(text="Add driver➕")],
        [KeyboardButton(text="Search company🔎"), KeyboardButton(text="Search driver🔎")],
        [KeyboardButton(text="Delete company❌"), KeyboardButton(text="Delete driver❌")],
        [KeyboardButton(text="Add money COMPANY"), KeyboardButton(text="Add money DRIVER")],
        [KeyboardButton(text="Send message to companies"), KeyboardButton(text="Send message to drivers")],
        [KeyboardButton(text="Add money to one company balance"), KeyboardButton(text="Add money to one driver balance")],
        [KeyboardButton(text="Set invite price for company"), KeyboardButton(text="Set invite price for driver")],
        [KeyboardButton(text="Set price for company"), KeyboardButton(text="Set price for driver")],
    ]
)

# company_callback = CallbackData("company", "action")


class CompanyCallback(CallbackData, prefix="company"):
    action: str


driver_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Cancel ❌",
                callback_data=CompanyCallback(action="cancel").pack(),
            ),
            InlineKeyboardButton(
                text="Next ➡️",
                callback_data=CompanyCallback(action="next").pack(),
            ),
        ]
    ]
)


class DriverCallback(CallbackData, prefix="driver"):
    action: str
    driver_id: int
    requested_company_id: int


# def create_company_keyboard(driver_id, company_id):
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(
#                     text="Cancel ❌",
#                     callback_data=DriverCallback(
#                         action="cancel",
#                         driver_id=driver_id,
#                         requested_company_id=company_id,
#                     ).pack(),
#                 ),
#                 InlineKeyboardButton(
#                     text="Send Request 📤",
#                     callback_data=DriverCallback(
#                         action="send",
#                         driver_id=driver_id,
#                         requested_company_id=company_id,
#                     ).pack(),
#                 ),
                
#                 InlineKeyboardButton(
#                     text="Next ➡️",
#                     callback_data=DriverCallback(
#                         action="next",
#                         driver_id=driver_id,
#                         requested_company_id=company_id,
#                     ).pack(),
#                 ),
#             ]
#         ]
#     )

#V2
def create_company_keyboard(driver_id, company_id): 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Send Request 📤",
                    callback_data=DriverCallback(
                        action="send",
                        driver_id=driver_id,
                        requested_company_id=company_id,
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Send Request for CDL📤",
                    callback_data=DriverCallback(
                        action="cdl",
                        driver_id=driver_id,
                        requested_company_id=company_id,
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Send Request for Medical card📤",
                    callback_data=DriverCallback(
                        action="medicalcard",
                        driver_id=driver_id,
                        requested_company_id=company_id,
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Cancel ❌",
                    callback_data=DriverCallback(
                        action="cancel",
                        driver_id=driver_id,
                        requested_company_id=company_id,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="Next ➡️",
                    callback_data=DriverCallback(
                        action="next",
                        driver_id=driver_id,
                        requested_company_id=company_id,
                    ).pack(),
                )
            ]
        ]
    )


def create_email_forward_keyboard(email: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Send Email 📧", url=f"mailto:{email}"),
            ]
        ]
    )


def create_telegram_forward_keyboard(chat_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Forward to Telegram 📲", callback_data=f"forward_{chat_id}"
                ),
            ]
        ]
    )


def create_telegram_user_keyboard(telegram_id: int, phone: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Open Telegram Chat 📩",
                    url=f"tg://user?id={telegram_id}",  # Telegram ID orqali shaxsiy chatga yo'naltirish
                )
                # InlineKeyboardButton(text="Call 📞", url=f"tel:+998970183595"),
            ]
        ]
    )


def create_combined_keyboard(telegram_id: int, email: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Open Telegram Chat 📩", url=f"tg://user?id={telegram_id}"
                ),
                InlineKeyboardButton(text="Send Email 📧", url=f"mailto:{email}"),
            ]
        ]
    )


company_tables = {
    "companies": "Company info",
    "CompanyDriverOffers": "Offer for company driver",
    "SpecialLoads": "Driver Load Offer Details",
    "LeaseDriverOffers": "Offer for lease driver",
    "OwnerDriverOffers": "Offer for owner driver",
}

driver_tables = {
    "drivers": "Driver info",
    # "cdls": "CDL",
    # "MedicalCards": "Medical Card"
}

companies_columns = {
    "company_name": "Company name",
    "dot": "DOT",
    "mc": "MC",
    "address": "Address",
    "current_trucks": "Trucks number",
    "company_email": "Company email",
    "company_contact": "Company contact"
}

CompanyDriverOffers_columns = {
    "driver_salary_for_solo_usd": "Driver salary for solo ($)",
    "driver_salary_for_solo_percentage": "Driver salary for solo (%)",
    "driver_salary_for_team_usd": "Driver salary for team ($)",
    "escrow_per_week": "Escrow per week",
    "escrow_total": "Escrow total",
    "layover": "Layover",
    "avaiable_truck_numbers": "Avaiable truck numbers",
    "avaiable_trucks_make": "Avaiable trucks make",
    "truck_speed": "Truck speed",
    "minimum_experience_requirement": "Minimum experience requirement"
}

SpecialLoads_columns = {
    "amazon": "Amazon",
    "po_loads": "PO Loads",
    "dry_van": "Dry Van",
    "line_loads": "Line loads",
}

LeaseDriverOffers_columns = {
    "truck_rental_fee": "Truck rental fee (%)",
    "truck_miles": "Truck Miles",
    "dispatch_service": "Dispatch service",
    "office_admin_usd": "Office admin ($)",
    "ifta": "IFTA",
    "insurance_type": "Insurance type",
    "insurance": "Insurance"
}

OwnerDriverOffers_columns = {
    "dispatch_service": "Dispatch service",
    "office_admin_usd": "Office admin ($)",
    "ifta": "IFTA",
    "insurance": "Insurance"
}

drivers_columns = {
    "driver_type": "Driver type",
    "first_name": "First name",
    "last_name": "Last name",
    "birth_day": "Birth day",
    "address": "Address",
    "email": "Email",
    "phone_number": "Phone number",
    "miles_dialy": "Miles Dialy",
    "miles_weekly": "Miles weekly",
    "work_days_type": "Work days type",
    "work_days": "Work days",
    "home_days": "Home days",
    "nigth_or_day_time_PU": "Night or day time PU"
}

cdls_columns = {
    "cdl": "CDL",
    "state_of_cdl": "State of cdl",
    "class": "Class",
    "expire_date": "Expire date",
    "issue_date": "Issue date"
}

MedicalCards_columns = {
    "national_registry": "National registry",
    "expiration_date": "Expiration date",
    "date_certificate_signed": "Certificate signed date"
}

