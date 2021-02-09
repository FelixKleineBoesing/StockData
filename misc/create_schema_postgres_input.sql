CREATE TABLE IF NOT EXISTS stock_data (
    index SERIAL PRIMARY KEY,
    date_time TIMESTAMP NOT NULL,
    price FLOAT,
    minute_return FLOAT,
    hour_return FLOAT,
    day_return FLOAT,
    stock_name VARCHAR NOT NULL);

CREATE TABLE IF NOT EXISTS meta_data (
    index SERIAL PRIMARY KEY,
    stock_name VARCHAR NOT NULL,
    drift FLOAT NOT NULL,
    volatility FLOAT NOT NULL);