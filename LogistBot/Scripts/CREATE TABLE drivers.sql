CREATE TABLE drivers(
    id BIGINT PRIMARY KEY,
    driver_type VARCHAR(256),
    first_name VARCHAR(256),
    last_name VARCHAR(256),
    birth_day VARCHAR(256), 
    address VARCHAR(256),
    email VARCHAR(256),
    phone_number VARCHAR(256),
    miles_dialy  VARCHAR(256) DEFAULT NULL,
    miles_weekly VARCHAR(256) DEFAULT NULL,
    work_days_type VARCHAR(256) DEFAULT NULL,
    work_days VARCHAR(256) DEFAULT NULL,
    home_days VARCHAR(256) DEFAULT NULL,
    nigth_or_day_time_PU VARCHAR(256) DEFAULT NULL
)