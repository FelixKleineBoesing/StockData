from pathlib import Path
import pandas as pd
from fkbutils.dbwrapper.postgres import PostgresWrapper
from fkbutils.misc.config_manager import ConfigManager

from src.generator import get_default_variables


def import_init_dataset(postgres_wrapper: PostgresWrapper,
                        stock_data_path: str = Path("..", "..", "data", "all_stocks_5yr.csv")):

    count = postgres_wrapper.get_query("Select count(*) from stock_data;", fetch=True).iloc[0, 0]
    if count > 0:
        raise AssertionError("Database is already initialised! Dump all volumes if you want to init a new db!")
    stock_data = pd.read_csv(stock_data_path)
    stock_data["date"] = pd.to_datetime(stock_data["date"])
    stock_data.drop(["high", "low", "close", "volume"], axis=1, inplace=True)
    stock_data.rename({"date": "date_time", "open": "price", "Name": "name"}, axis=1, inplace=True)

    postgres_wrapper.insert_from_df(data=stock_data, table_name="stock_data", commit=True)


def get_postgres_wrapper(config_manager: ConfigManager):
    return PostgresWrapper(host=config_manager.get_value("POSTGRES_INPUT_HOST"),
                           port=config_manager.get_value("POSTGRES_INPUT_PORT"),
                           user=config_manager.get_value("POSTGRES_INPUT_USER"),
                           password=config_manager.get_value("POSTGRES_INPUT_PASSWORD"),
                           dbname=config_manager.get_value("POSTGRES_INPUT_DB"),
                           )


if __name__ == "__main__":
    config = ConfigManager(default_variables=get_default_variables(), env_file=Path("../../.env"))
    pwrapper = get_postgres_wrapper(config_manager=config)
    import_init_dataset(pwrapper)
