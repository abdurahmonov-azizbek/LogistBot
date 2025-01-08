-- CREATE TABLE SpecialLoads (
--     id BIGINT PRIMARY KEY, 
--     amazon VARCHAR(20) DEFAULT NULL,
--     po_loads VARCHAR(20) DEFAULT NULL,
--     dry_van VARCHAR(20) DEFAULT NULL,
--     broker_loads VARCHAR(20) DEFAULT NULL,
--     line_loads VARCHAR(20) DEFAULT NULL
-- );

CREATE TABLE SpecialLoads (
    id BIGINT PRIMARY KEY, 
    amazon VARCHAR(20) DEFAULT NULL,
    po_loads VARCHAR(20) DEFAULT NULL,
    dry_van VARCHAR(20) DEFAULT NULL,
    line_loads VARCHAR(20) DEFAULT NULL
)