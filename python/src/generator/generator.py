import logging

import numpy as np
import pandas as pd
from fkbutils.dbwrapper import PostgresWrapper
from scipy.stats import norm
from datetime import timedelta


def generate_next_price(current_price: float, drift: float, vola: float, external_term: float, var_dist):
    error_term = var_dist.rvs(1)[0]
    return current_price * (1 + drift + error_term * vola + external_term)


def generate_new_prices(postgres: PostgresWrapper, batch_size: int = 120):
    """

    :param postgres:
    :return:
    """
    meta_data = postgres.get_table(table_name="meta_data")
    name_index, val_index, drift_index = \
        meta_data.columns.get_loc("stock_name"), \
        meta_data.columns.get_loc("volatility"), \
        meta_data.columns.get_loc("drift")

    meta_data = {
        meta_data.iloc[i, name_index]: {
            "sd": meta_data.iloc[i, val_index],
            "drift": meta_data.iloc[i, drift_index]
        } for i in range(meta_data.shape[0])
    }

    last_prices = postgres.get_query(query="""
        SELECT t.stock_name, t.price, r.Maxdate
        FROM (
              SELECT stock_name, MAX(date_time) as Maxdate
              FROM stock_data
              GROUP BY stock_name
        ) r
        INNER JOIN stock_data t
        ON t.stock_name = r.stock_name AND t.date_time = r.Maxdate""")

    name_index, price_index, date_index = \
        last_prices.columns.get_loc("stock_name"), \
        last_prices.columns.get_loc("price"), \
        last_prices.columns.get_loc("maxdate")

    last_prices = {
        last_prices.iloc[i, name_index]: {
            "price": last_prices.iloc[i, price_index],
            "date": last_prices.iloc[i, date_index]
        } for i in range(last_prices.shape[0])
    }
    new_prices = []
    norm_dist = norm(loc=0, scale=1)

    i = 0
    while True:
        for name in last_prices.keys():
            new_price = generate_next_price(
                last_prices[name]["price"], meta_data[name]["drift"], meta_data[name]["sd"], 0.0, norm_dist
            )
            new_date = last_prices[name]["date"] + timedelta(minutes=1)
            new_prices.append({
                "stock_name": name, "price": new_price, "date_time": new_date
            })
            last_prices[name] = {"price": new_price, "date": new_date}
        i += 1
        if i >= batch_size:
            postgres.insert_from_df(pd.DataFrame(new_prices), table_name="stock_data", commit=True)
            logging.info("Inserted a new batch of prices into the database!")
            new_prices = []
