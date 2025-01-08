-- CREATE TABLE LeaseDriverOffers(
--     id BIGINT PRIMARY KEY,
--     truck_rental_fee_type VARCHAR(256), -- PER WEEK/MONTH
--     truck_rental_fee VARCHAR(256),
--     truck_miles VARCHAR(256), -- PER MILE
--     dispatch_service VARCHAR(256),
--     safety_service_type VARCHAR(256), --$
--     safety_service VARCHAR(256), -- %
--     office_admin_type VARCHAR(256), -- $
--     office_admin VARCHAR(256), -- % xxxx
--     ifta VARCHAR(256),
--     insurance_type VARCHAR(256), -- PER WEEK/MONTH
--     insurance VARCHAR(256)
-- )

CREATE TABLE LeaseDriverOffers(
    id BIGINT PRIMARY KEY,
    truck_rental_fee VARCHAR(256),
    truck_miles VARCHAR(256), -- PER MILE
    dispatch_service VARCHAR(256),
    office_admin_usd VARCHAR(256), -- $
    ifta VARCHAR(256),
    insurance_type VARCHAR(256), -- PER WEEK/MONTH
    insurance VARCHAR(256)
)