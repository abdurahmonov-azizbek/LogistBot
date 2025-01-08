-- CREATE TABLE CompanyDriverOffers(
-- id BIGINT PRIMARY KEY,
-- driver_salary_for_solo_type VARCHAR(256), -- $
-- driver_salary_for_solo VARChAR(256),      -- %
-- driver_salary_for_team_type VARCHAR(256), -- $
-- driver_salary_for_team VARCHAR(256),      -- %
-- escrow_per_week VARCHAR(256),
-- escrow_total VARCHAR(256),
-- layover VARCHAR(256),
-- detension_for_each_extra_stop VARCHAR(256),
-- avaiable_truck_numbers VARCHAR(256),
-- avaiable_trucks_make VARCHAR(256),
-- truck_speed VARCHAR(256),
-- minimum_experience_requirement VARCHAR(512)
-- )

CREATE TABLE CompanyDriverOffers(
id BIGINT PRIMARY KEY,
driver_salary_for_solo_usd VARCHAR(256), -- $
driver_salary_for_solo_percentage VARChAR(256),      -- %
driver_salary_for_team_usd VARCHAR(256), -- $
escrow_per_week VARCHAR(256),
escrow_total VARCHAR(256),
layover VARCHAR(256),
avaiable_truck_numbers VARCHAR(256),
avaiable_trucks_make VARCHAR(256),
truck_speed VARCHAR(256),
minimum_experience_requirement VARCHAR(512)
)   