CREATE TABLE IF NOT EXISTS settings(
    daily_price_for_company FLOAT NOT NULL DEFAULT 0,
    daily_price_for_driver FLOAT NOT NULL DEFAULT 0,
    referal_price_for_company FLOAT NOT NULL DEFAULT 0,
    referal_price_for_driver FLOAT NOT NULL DEFAULT 0
);

INSERT INTO settings(daily_price_for_company, daily_price_for_driver, referal_price_for_company, referal_price_for_driver)
VALUES (0, 0, 0, 0)