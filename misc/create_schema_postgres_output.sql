CREATE TABLE IF NOT EXISTS stock_data (
    index SERIAL PRIMARY KEY,
    date_time TIMESTAMP NOT NULL,
    price FLOAT,
    name VARCHAR NOT NULL);
CREATE INDEX date_time_stock_data ON stock_data.date_time;

CREATE TABLE IF NOT EXISTS generator_logging (
    index SERIAL PRIMARY KEY,
    date_time TIMESTAMP NOT NULL,
    log_text VARCHAR NOT NULL,
    status VARCHAR NOT NULL);