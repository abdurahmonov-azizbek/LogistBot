CREATE TABLE cdls(
	id BIGINT PRIMARY KEY,
	cdl VARCHAR(256),
	state_of_cdl VARCHAR(256),
	class VARCHAR(256),
	expire_date VARCHAR(256), -- month/day/year
	issue_date VARCHAR(256) -- month/day/year
)