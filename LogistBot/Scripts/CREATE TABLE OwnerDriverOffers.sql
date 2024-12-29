CREATE TABLE OwnerDriverOffers(
    id BIGINT PRIMARY KEY,
    dispatch_service VARCHAR(256),
    safety_service_type VARCHAR(256), -- $
    safety_service VARCHAR(256),      -- %
    office_admin_type VARCHAR(256), -- $
    office_admin VARCHAR(256), -- % xxxx
    ifta VARCHAR(256),
    insurance_type VARCHAR(256),
    insurance VARCHAR(256)
)