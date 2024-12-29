CREATE TABLE companies (
    id BIGINT PRIMARY KEY,           -- Telegram foydalanuvchi ID (unikal va asosiy kalit)
    company_name VARCHAR(255) NOT NULL,      -- Kompaniya nomi
    dot VARCHAR(50) NOT NULL,                -- DOT raqami
    mc VARCHAR(50) NOT NULL,                 -- MC raqami
    address TEXT NOT NULL,                   -- Kompaniya manzili (shahar, davlat va ZIP kodi bilan)
    current_trucks INT DEFAULT 0,            -- Hozirgi mavjud yuk mashinalari soni
    company_email VARCHAR(255) NOT NULL,     -- Kompaniya emaili
    company_contact VARCHAR(50) NOT NULL     -- Kompaniya telefon raqami
);
