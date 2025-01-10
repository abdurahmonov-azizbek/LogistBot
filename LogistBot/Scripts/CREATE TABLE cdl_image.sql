CREATE TABLE cdl_image(
    id BIGINT NOT NULL,
    unique_id SERIAL NOT NULL,
    front_side VARCHAR(200),
    back_side VARCHAR(200),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)