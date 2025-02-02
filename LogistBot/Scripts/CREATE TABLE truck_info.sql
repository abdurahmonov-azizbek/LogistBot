-- Only for owner drivers
CREATE TABLE truck_info(
	id BIGINT PRIMARY KEY NOT NULL,
	unit_number VARCHAR(100) NOT NULL,
	truck_make VARCHAR(100) NOT NULL,
	truck_model VARCHAR(100) NOT NULL,
	truck_year VARCHAR(100) NOT NULL,
	registered_state VARCHAR(100) NOT NULl
)