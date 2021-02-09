CREATE TABLE IF NOT EXISTS stock_data (
    index SERIAL PRIMARY KEY,
    date_time TIMESTAMP NOT NULL,
    price FLOAT,
    stock_name VARCHAR NOT NULL);

CREATE TABLE IF NOT EXISTS generator_logging (
    index SERIAL PRIMARY KEY,
    date_time TIMESTAMP NOT NULL,
    log_text VARCHAR NOT NULL,
    status VARCHAR NOT NULL);