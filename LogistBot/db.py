import asyncpg
import config


async def get_db_connection():
    return await asyncpg.connect(**config.DB_CONFIG)

async def save_lease_driver_offer(data: dict):
    conn = await get_db_connection()

    query = """
        INSERT INTO LeaseDriverOffers (id, truck_rental_fee, truck_miles, dispatch_service, office_admin_usd, ifta, insurance_type, insurance)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """

    await conn.execute(
        query,
        data['id'],
        data['TruckRentalFee'],
        data['TruckMiles'],
        data['DispatchService'],
        data['OfficeAdminUsd'],
        data['Ifta'],
        data['InsuranceType'],
        data['Insurance']
    )

    await conn.close()

async def save_driver(data: dict):
    conn = await get_db_connection()
    query = """
        INSERT INTO drivers (id, driver_type, first_name, last_name, birth_day, address, email, phone_number)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """

    await conn.execute(
        query,
        data['id'],
        data['DriverType'],
        data['FirstName'],
        data['LastName'],
        data['BirthDay'],
        data['Address'],
        data['Email'],
        data['PhoneNumber']
    )

    await conn.close()

# async def save_default_driver_filter(id):
#     conn = await get_db_connection()
#     query = """
#         INSERT INTO CompanyStatus (id, is_active, company_driver, owner_driver, lease_driver)
#         VALUES ($1, $2, $3, $4, $5)
#     """

#     await conn.execute(
#         query,
#         id,
#         True,
#         True,
#         True,
#         True
#     )

#     await conn.close()

async def save_driver_status(id, status: bool):
    conn = await get_db_connection()
    query = "INSERT INTO DriverStatus (id, is_active) VALUES ($1, $2)"

    await conn.execute(query, id, status)


async def save_company_status(id, status: bool):
    conn = await get_db_connection()
    query = "INSERT INTO CompanyStatus (id, is_active) VALUES ($1, $2)"

    await conn.execute(query, id, status)

async def update_driver_status(id, status: bool):
    conn = await get_db_connection()
    query = "UPDATE DriverStatus SET is_active=$1 WHERE id=$2"

    await conn.execute(query, status, id)

async def update_company_status(id, status: bool):
    conn = await get_db_connection()
    query = "UPDATE CompanyStatus SET is_active=$1 WHERE id=$2"

    await conn.execute(query, status, id)


async def update_driver_filter(data: dict):
    conn = await get_db_connection()
    query = """
    UPDATE CompanyStatus
    SET 
        is_active=$1,
        company_driver=$2,
        owner_driver=$3, 
        lease_driver=$4
    WHERE id=$5
    """

    await conn.execute(
        query,
        data['IsActive'].lower() == "active",
        data['CompanyDriver'] == "YES",
        data['OwnerDriver'] == "YES",
        data['LeaseDriver'] == "YES",
        data['id']
    )

    await conn.close()

async def save_owner_driver_offer(data: dict):
    conn = await get_db_connection()
    query = """
        INSERT INTO OwnerDriverOffers (id, dispatch_service, office_admin_usd, ifta, insurance)
        VALUES ($1, $2, $3, $4, $5)
    """

    await conn.execute(
        query,
        data['id'],
        data['DispatchService'],
        data['OfficeAdmin'],
        data['Ifta'],
        data['Insurance']
    )

    await conn.close()

async def save_carrier_data(data: dict):
    conn = await get_db_connection()
    query = """
        INSERT INTO companies (id, company_name, dot, mc, address, current_trucks, company_email, company_contact)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """

    await conn.execute(
        query,
        data["id"],
        data["company_name"],
        data["dot"],
        data["mc"],
        data["address"],
        data["current_trucks"],
        data["company_email"],
        data["company_contact"]
    )

    await conn.close()


async def get_all_companies():
    conn = await get_db_connection()
    query = """
        SELECT c.* 
        FROM companies AS c
        JOIN CompanyStatus AS cs ON c.id = cs.id
        WHERE cs.is_active = true"""
    
    try:
        rows = await conn.fetch(query)  # barcha yozuvlarni olish
        return [dict(row) for row in rows]  # natijani dict ko'rinishida qaytarish
    except Exception as e:
        print(f"[*] Error fetching all companies: {e}")
        return []
    finally:
        await conn.close()


async def set_company_filter(id, driver_type):
    try:
        conn = await get_db_connection()
        old = await get_by_id(id, "CompanyFilter")
        if old:
            await delete_by_id(id, "CompanyFilter")
        
        query = "INSERT INTO CompanyFilter (id, driver_type) VALUES ($1, $2)"
        await conn.execute(query, id, driver_type)
    except Exception as e:
        print(e)
    finally:
        await conn.close()


async def get_all_drivers(driver_type: str = None):
    conn = await get_db_connection()
    query = """
        SELECT d.*
        FROM drivers AS d
        JOIN DriverStatus AS ds ON d.id = ds.id
        WHERE ds.is_active = true
    """
    
    # Add condition dynamically if driver_type is provided
    if driver_type is not None:
        query += " AND d.driver_type = $1"
    
    try:
        # Use a parameterized query to prevent SQL injection
        if driver_type is None:
            rows = await conn.fetch(query)  # Fetch all active drivers
        else:
            rows = await conn.fetch(query, driver_type)  # Pass driver_type as a parameter
        
        return [dict(row) for row in rows]  # Return results as a list of dictionaries
    except Exception as e:
        print(f"[*] Error fetching all drivers: {e}")
        return []
    finally:
        await conn.close()



async def save_company_driver_offer(data: dict):
    conn = await get_db_connection()
    query = """
        INSERT INTO CompanyDriverOffers (id, driver_salary_for_solo_usd, driver_salary_for_solo_percentage, driver_salary_for_team_usd, escrow_per_week, escrow_total, layover, avaiable_truck_numbers, avaiable_trucks_make, truck_speed, minimum_experience_requirement)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    """

    await conn.execute(
        query,
        data['id'],
        data['DriverSalaryForSoloUsd'],
        data['DriverSalaryForSoloPercentage'],
        data['DriverSalaryForTeamUsd'],
        data['EscrowPerWeek'],
        data['EscrowTotal'],
        data['Layover'],
        data['AvaiableTruckNumbers'],
        data['AvaiableTrucksMake'],
        data['TruckSpeed'],
        data['MinimumExperienceRequirement']
    )

    await conn.close()

async def save_special_loads(data: dict):
    conn = await get_db_connection()
    query = """
        INSERT INTO SpecialLoads (id, amazon, po_loads, dry_van, line_loads)
        VALUES ($1, $2, $3, $4, $5)
    """

    await conn.execute(
        query,
        data["id"],
        data["amazon"],
        data["po_loads"],
        data["dry_van"],
        data["line_loads"]
    )

    await conn.close()

async def get_by_id(id: int, table_name: str, id_column: str = "id"):
    try:
        conn = await get_db_connection()
        query = f"SELECT * FROM {table_name} WHERE {id_column} = $1"
        row = await conn.fetchrow(query, id)

        if row:
            return dict(row)
        else:
            return None
        
    except Exception as e:
        print(f"[*] Error fetching: {e}")
    finally:
        await conn.close()

async def get_latest_by_date(user_id, table_name: str, date_column: str = "created_at"):
    """
    Sana bo'yicha eng oxirgi yaratilgan obyektni qaytaradi.

    :param table_name: Jadval nomi
    :param date_column: Sana ustuni nomi (standart: "created_at")
    :return: Eng oxirgi obyekt yoki None
    """
    try:
        conn = await get_db_connection()
        query = f"""
        SELECT * 
        FROM {table_name}
        WHERE id = $1
        ORDER BY {date_column} DESC
        LIMIT 1
        """
        row = await conn.fetchrow(query, user_id)

        if row:
            return dict(row)
        else:
            return None
        
    except Exception as e:
        print(f"[*] Error fetching latest record: {e}")
    finally:
        await conn.close()


async def delete_by_id(id: int, table_name: str, id_column: str = "id") -> bool:
    """
    Ma'lum id bo'yicha satrni o'chirish.
    :param id: O'chirilishi kerak bo'lgan ID (BIGINT diapazonida bo'lishi kerak).
    :param table_name: Jadval nomi.
    :param id_column: ID ustuni nomi.
    :return: O'chirish muvaffaqiyatli bo'lsa True, aks holda False.
    """
    try:
        conn = await get_db_connection()
        query = f"DELETE FROM {table_name} WHERE {id_column} = $1"
        row = await conn.execute(query, id)
        # `conn.execute` string qaytaradi, uni tekshirish kerak
        if row and "DELETE" in row:
            return True
        else:
            return False
    except Exception as e:
        print(f"[!] Error deleting row: {e}")
    finally:
        await conn.close()

         
async def save_company_driver_more_info(data: dict):
    conn = await get_db_connection()
    
    driver = await get_by_id(data['id'], "drivers")
    if not driver:
        return None
    
    query = f"""
    UPDATE drivers
    SET miles_dialy=$1, miles_weekly=$2, work_days_type=$3, work_days=$4, home_days=$5, nigth_or_day_time_PU=$6
    WHERE id = {data['id']}
    """
    
    await conn.execute(
        query,
        data['MilesDialy'],
        data['MilesWeekly'],
        data['WorkDaysType'],
        data['WorkDays'],
        data['HomeDays'],
        data['NightOrDayTimePU']
    )
    
    await conn.close()
    
async def save_cdl(data: dict):
    conn = await get_db_connection()
    
    query = """
        INSERT INTO cdls (id, cdl, state_of_cdl, class, expire_date, issue_date)
        VALUES ($1, $2, $3, $4, $5, $6)
    """
    
    await conn.execute(
        query,
        data['id'],
        data['Cdl'],
        data['StateOfCdl'],
        data['Class'],
        data['ExpireDate'],
        data['IssueDate']
    )
    
    await conn.close()

async def save_medical_card(data: dict):
    conn = await get_db_connection()

    query = """
        INSERT INTO MedicalCards (id, national_registry, expiration_date, date_certificate_signed)
        VALUES ($1, $2, $3, $4)
    """

    await conn.execute(
        query,
        data['id'],
        data['NationalRegistry'],
        data['ExpirationDate'],
        data['DateCertificateSigned']
    )

    await conn.close()

async def save_driver_note(data: dict):
    conn = await get_db_connection()

    query = """
        INSERT INTO DriverNotes (id, note) 
        VALUES ($1, $2)
    """

    await conn.execute(
        query,
        data['id'],
        data['note']
    )

    await conn.close()


async def get_one_column(table: str, column: str, id: int) -> str:
    # Validate table and column names (to prevent SQL injection)
    if not table.isidentifier() or not column.isidentifier():
        raise ValueError("Invalid table or column name")

    # Connect to the database
    conn = await get_db_connection()
    try:
        # Use string interpolation for table/column and parameters for values
        query = f"SELECT {column} FROM {table} WHERE id = $1"
        row = await conn.fetchrow(query, id)
        if row:
            return row[column]
        return None
    finally:
        await conn.close()

async def get_rows_count(table_name: str):
    try:
        conn = await get_db_connection()
        row = await conn.fetchrow(f"SELECT COUNT(*) FROM {table_name}")
        if row:
            return row[0]
        return 0
    finally:
        await conn.close()


async def update_one_column(id, table, column, value):
    # Validate table and column names (to prevent SQL injection)
    if not table.isidentifier() or not column.isidentifier():
        raise ValueError("Invalid table or column name")
    
    # Connect to the database
    conn = await get_db_connection()
    try:
        # Use string interpolation for table/column and parameterization for values
        query = f"UPDATE {table} SET {column} = $1 WHERE id = $2"
        
        # Execute the query with parameterized values
        await conn.execute(query, value, id)
    finally:
        await conn.close()


async def search_company(key):
    try:
        conn = await get_db_connection()
        
        # Prepare the query and parameters
        if key.isdigit():
            query = "SELECT * FROM companies WHERE id = $1"
            params = (int(key),)
        else:
            query = "SELECT * FROM companies WHERE LOWER(company_name) LIKE $1"
            params = (f"%{key.lower()}%",)

        # Execute the query
        result = await conn.fetch(query, *params)

        # Convert rows to dictionary
        return [dict(row) for row in result]
    except Exception as e:
        print(f"[*] Error searching company: {e}")
        return []
    finally:
        if conn:
            await conn.close()

async def search_driver(key):
    try:
        conn = await get_db_connection()
        
        # Prepare the query and parameters
        if key.isdigit():
            query = "SELECT * FROM drivers WHERE id = $1"
            params = (int(key),)
        else:
            query = "SELECT * FROM drivers WHERE LOWER(first_name) LIKE $1 OR LOWER(last_name) LIKE $1"
            params = (f"%{key.lower()}%",)

        # Execute the query
        result = await conn.fetch(query, *params)

        # Convert rows to dictionary
        return [dict(row) for row in result]
    except Exception as e:
        print(f"[*] Error searching driver: {e}")
        return []
    finally:
        if conn:
            await conn.close()

async def save_cdl_image(data: dict):
    try:
        conn = await get_db_connection()
        query = "INSERT INTO cdl_image (id, front_side, back_side) VALUES ($1, $2, $3)"
        await conn.execute(
            query,
            data['id'],
            data['front_side'],
            data['back_side']
        )
        
    except Exception as ex:
        print(f"[!] Error saving cdl images: {ex}")

async def save_medical_card_image(data: dict):
    try:
        conn = await get_db_connection()
        query = "INSERT INTO medical_card_image (id, file_path) VALUES ($1, $2)"
        await conn.execute(query, data['id'], data['file_path'])
    except Exception as e:
        print(f"[!] Error saving medical card images: {e}")


async def save_company_balance(id, balance):
    try:
        conn = await get_db_connection()
        query = "INSERT INTO CompanyBalance (id, balance) VALUES ($1, $2)"
        await conn.execute(query, id, balance)
    except Exception as e:
        print(f"[!] Error saving CompanyBalance: {e}")

async def save_driver_balance(id, balance):
    try:
        conn = await get_db_connection()
        query = "INSERT INTO DriverBalance (id, balance) VALUES ($1, $2)"
        await conn.execute(query, id, balance)
    except Exception as e:
        print(f"[!] Error saving CompanyBalance: {e}")

async def get_all(table_name):
    conn = await get_db_connection()
    query = f"SELECT * FROM {table_name}"
    
    try:
        rows = await conn.fetch(query)  # barcha yozuvlarni olish
        return [dict(row) for row in rows]  # natijani dict ko'rinishida qaytarish
    except Exception as e:
        print(f"[*] Error fetching all {table_name}: {e}")
        return []
    finally:
        await conn.close()


async def update_balance(table_name, id, new_balance):
    conn = await get_db_connection()
    try:
        query = f"UPDATE {table_name} SET balance = $1 WHERE id = $2"
        
        await conn.execute(query, new_balance, id)
    finally:
        await conn.close()


async def get_settings():
    try:
        conn = await get_db_connection()
        query = f"SELECT * FROM settings LIMIT 1"
        row = await conn.fetchrow(query)

        if row:
            return dict(row)
        else:
            raise Exception("Settings not found!")
    except Exception as ex:
        print(ex)
    finally:
        await conn.close()


async def update_settings(column, value):
    try:
        conn = await get_db_connection()
        query = f"UPDATE settings SET {column} = $1"
        await conn.execute(query, value)
    except Exception as e:
        print(e)
    finally:
        await conn.close()

async def save_referal(id, invited_id):
    try:
        conn = await get_db_connection()
        query = "INSERT INTO referals(id, invited_user_id) VALUES ($1, $2)"
        await conn.execute(query, id, invited_id)
    except Exception as e:
        print(e)
    finally:
        await conn.close()

async def save_truck_info(data: dict):
    try:
        conn = await get_db_connection()
        query = "INSERT INTO truck_info(id, unit_number, truck_make, truck_model, truck_year, registered_state) VALUES ($1, $2, $3, $4, $5, $6)"
        await conn.execute(
            query,
            data['id'],
            data['UnitNumber'],
            data['TruckMake'],
            data['TruckModel'],
            data['TruckYear'],
            data['RegisteredState']
        )
    except Exception as e:
        print(e)
    finally:
        await conn.close()