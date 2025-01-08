from db import *
from keyboars import *
import os


async def get_company_full_info(company: dict, user_id):
    info = []
    
    company_information = f"Company Infoℹ️\nId: {company['id']}\nCompany name: {company['company_name']}\nDOT: {company['dot']}\nMC: {company['mc']}\nAddress: {company['address']}\nTrucks: {company['current_trucks']}\nEmail: {company['company_email']}\nContact: {company['company_contact']}"
    info.append(company_information)

    special_load = await get_by_id(user_id, "SpecialLoads")

    if special_load:
        info.append(f"Special loadsℹ️\n{getNameForSpecialLoad("Amazon", special_load['amazon'])}{getNameForSpecialLoad("PO Loads", special_load['po_loads'])}{getNameForSpecialLoad("Dry Van", special_load['dry_van'])}{getNameForSpecialLoad("Line Loads", special_load['line_loads'])}")
    
    company_driver_offer = await get_by_id(user_id, "CompanyDriverOffers")
    if company_driver_offer:
        info.append(f"Offer for Company driverℹ️\nDriver salary for solo {company_driver_offer['driver_salary_for_solo_usd']}$ or {company_driver_offer['driver_salary_for_solo_percentage']}%\nDriver salary for team: {company_driver_offer['driver_salary_for_team_usd']}$\nEscrow per week: {company_driver_offer['escrow_per_week']}$\nEscrow total: {company_driver_offer['escrow_total']}$\nLayover: {company_driver_offer['layover']}$\nTruck numbers: {company_driver_offer['avaiable_truck_numbers']}\nAvaiable trucks make: {company_driver_offer['avaiable_trucks_make']}\nTruck speed: {company_driver_offer['truck_speed']}\nMinimum experience requirement: {company_driver_offer['minimum_experience_requirement']}")

    owner_driver = await get_by_id(user_id, "OwnerDriverOffers")
    if owner_driver:
        info.append(f"Offer for Owner driverℹ️\n\nDispatch Service: {owner_driver['dispatch_service']}\nOffice admin: {owner_driver['office_admin_usd']}\nIFTA: {owner_driver['ifta']}\nInsuranse: {owner_driver['insurance']}")

    lease = await get_by_id(user_id, "LeaseDriverOffers")
    if lease:
        info.append(f"Offer for lease driverℹ️\n\nTruck rental fee: {lease['truck_rental_fee']}\nTruck miles: {lease['truck_miles']}\nDispatch service: {lease['dispatch_service']}\nOffice admin: {lease['office_admin_usd']}$\nIFTA: {lease['ifta']}\nInsurance: {lease['insurance']} {lease['insurance_type']}")

    return info


def getNameForSpecialLoad(pref, a):
    if a.lower() == "yes":
        return f"{pref}: YES\n"
    elif a.lower() == "no":
        return f"{pref}: NO\n"

    return ""


async def get_driver_full_info(driver: dict, user_id) -> str:
    info = []
    driver_information = f"ℹ️Driver info\nID: {driver['id']}\nDriver type: {driver['driver_type']}\nFirst name: {driver['first_name']}\nLast name: {driver['last_name']}\nBirth date: {driver['birth_day']}\nAddress: {driver['address']}\nEmail: {driver['email']}\nPhone number: {driver['phone_number']}"
    info.append(driver_information)
    cdl = await get_by_id(user_id, "cdls")
    if cdl:
        info.append(f"ℹ️CDL\n\nCDL: {cdl['cdl']}\nState of CDL: {cdl['state_of_cdl']}\nClass: {cdl['class']}\nExpire Date: {cdl['expire_date']}\nIssue Date: {cdl['issue_date']}")

    medical_card = await get_by_id(user_id, "MedicalCards")
    if medical_card:
        info.append(f"\nℹ️Medical card\nNational Registry: {medical_card['national_registry']}\nExpiration Date: {medical_card['expiration_date']}\nDate of Certificate {medical_card['date_certificate_signed']}")

    return driver_information


async def GetMainMenu(user_id):
    company = await get_by_id(user_id, "companies")
    if company:
        return carrier_main_menu
    
    driver = await get_by_id(user_id, "drivers")
    if driver:
        return driver_main_menu
    
async def checkAdmin(user_id) -> bool:
    return user_id in config.ADMINS


async def deleteAllData(user_id):
    try:
        company = await get_by_id(user_id, "companies")
        if company:
            await delete_by_id(user_id, "companies")
                
        companyDriverOffers = await get_by_id(user_id, "CompanydriverOffers")
        if companyDriverOffers:
            await delete_by_id(user_id, "CompanyDriverOffers")

        driver = await get_by_id(user_id, "drivers")
        if driver:
            await delete_by_id(user_id, "drivers")

        leaseDriverOffer = await get_by_id(user_id, "LeaseDriverOffers")
        if leaseDriverOffer:
            await delete_by_id(user_id, "LeaseDriverOffers")            

        ownerDriverOffer = await get_by_id(user_id, "OwnerDriverOffers")
        if ownerDriverOffer:
            await delete_by_id(user_id, "OwnerDriverOffers")
            
        specialLoads = await get_by_id(user_id, "SpecialLoads")
        if specialLoads:
            await delete_by_id(user_id, "SpecialLoads")

        cdl = await get_by_id(user_id, "cdls")
        if cdl:
            await delete_by_id(user_id, "cdls")

        medicalCard = await get_by_id(user_id, "MedicalCards")
        if medicalCard:
            await delete_by_id(user_id, "MedicalCards")

        companyStatus = await get_by_id(user_id, "CompanyStatus")
        if companyStatus:
            await delete_by_id(user_id, "CompanyStatus")

        driver_note = await get_by_id(user_id, "DriverNotes")
        if driver_note:
            await delete_by_id(user_id, "DriverNotes")

        driver_status = await get_by_id(user_id, "DriverStatus")
        if driver_status:
            await delete_by_id(user_id, "DriverStatus")
    except Exception as ex:
        print(f"Exception while erasing: {ex}")
        
async def create_cdl_folder(user_id):
    try:
        path = f"/Images/cdl/{user_id}"
        if not os.path.exists(path=path):
            os.makedirs(path)
    except Exception as ex:
        print(ex)