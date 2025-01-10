CREATE TABLE IF NOT EXISTS CompanyStatus(
    id BIGINT PRIMARY KEY,
    is_active boolean default false,
    company_driver boolean default true,
    owner_driver boolean default true,
    lease_driver boolean default true
)