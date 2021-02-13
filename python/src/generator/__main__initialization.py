import logging
from pathlib import Path
import pandas as pd
import numpy as np
from fkbutils.dbwrapper.postgres import PostgresWrapper
from fkbutils.misc.config_manager import ConfigManager

from src import get_default_variables
from src.misc.helpers import get_postgres_wrapper


def import_init_dataset(postgres_wrapper: PostgresWrapper,
                        stock_data_path: str = Path("..", "..", "data", "all_stocks_5yr.csv")):

    count = postgres_wrapper.get_query("Select count(*) from stock_data;", fetch=True).iloc[0, 0]
    if count > 0:
        logging.warning("Database is already initialised! Dump all volumes if you want to init a new db!")
        return
    stock_data = pd.read_csv(stock_data_path)
    stock_data["date"] = pd.to_datetime(stock_data["date"])
    stock_data = calculate_returns_per_minute(stock_data)
    stock_data.drop(["high", "low", "close", "volume"], axis=1, inplace=True)
    stock_data.rename({"date": "date_time", "open": "price", "Name": "stock_name"}, axis=1, inplace=True)

    meta_data = generate_meta_data(stock_data=stock_data)

    postgres_wrapper.insert_from_df(data=stock_data, table_name="stock_data", commit=True)
    postgres_wrapper.insert_from_df(data=meta_data, table_name="meta_data", commit=True)


def calculate_returns_per_minute(stock_data):
    number_minutes_per_day = 24 * 60
    array_minute_returns = [np.NaN]
    array_hour_returns = [np.NaN]
    array_day_returns = [np.NaN]
    stock_data.sort_values(["Name", "open"], ascending=[True, True], inplace=True)
    prices = stock_data["open"].values
    names = stock_data["Name"].values

    for i in range(1, stock_data.shape[0]):
        if names[i] != names[i-1]:
            array_minute_returns.append(np.NaN)
            array_hour_returns.append(np.NaN)
            array_day_returns.append(np.NaN)
        else:
            daily_return = (prices[i] - prices[i - 1]) / prices[i - 1]
            minute_return = np.power((daily_return + 1), 1 / number_minutes_per_day) - 1
            hour_return = np.power((daily_return + 1), 1 / 24) - 1
            array_minute_returns.append(minute_return)
            array_hour_returns.append(hour_return)
            array_day_returns.append(daily_return)

    stock_data["minute_return"] = array_minute_returns
    stock_data["hour_return"] = array_hour_returns
    stock_data["day_return"] = array_day_returns

    return stock_data


def generate_meta_data(stock_data):
    aggregated_values = []
    for name in pd.unique(stock_data["stock_name"]):
        aggregated_values.append({
            "stock_name": name,
            "drift": np.nanmean(stock_data.loc[stock_data["stock_name"] == name, "minute_return"]),
            "volatility": np.nanstd(stock_data.loc[stock_data["stock_name"] == name, "minute_return"])
        })
    return pd.DataFrame(aggregated_values)


if __name__ == "__main__":
    config = ConfigManager(default_variables=get_default_variables(), env_file=Path("../../.env"))
    pwrapper = get_postgres_wrapper(config_manager=config)
    import_init_dataset(pwrapper)
