from pathlib import Path

import requests as re
import datetime
import json

from fkbutils.misc import ConfigManager

from src.configurator.connect_configs import get_postgres_sink, get_postgres_source
from src import get_default_variables


def send_config_to_kafka_connect(config, timeout: int = 200, host: str = "localhost", port: int = 8083):
    start = datetime.datetime.now()
    while (start - datetime.datetime.now()).total_seconds() < timeout:
        try:
            res = re.post("http://{}:{}/connectors".format(host, port), headers={"Accept": "application/json"},
                          json=config)
            if res.status_code in [200, 201]:
                break
        except Exception as e:
            pass


if __name__ == "__main__":
    config_manager = ConfigManager(
        default_variables=get_default_variables(),
        env_file=Path("../../.env")
    )
    postgres_sink = get_postgres_sink(
        postgres_host=config_manager.get_value("POSTGRES_OUTPUT_HOST"),
        postgres_port=config_manager.get_value("POSTGRES_OUTPUT_PORT"),
        postgres_db=config_manager.get_value("POSTGRES_OUTPUT_DB"),
        postgres_user=config_manager.get_value("POSTGRES_OUTPUT_USER"),
        postgres_password=config_manager.get_value("POSTGRES_OUTPUT_PASSWORD"),
        schema_host=config_manager.get_value("SCHEMA_HOST"),
        schema_port=config_manager.get_value("SCHEMA_PORT")
    )
    postgres_source = get_postgres_source(
        postgres_host=config_manager.get_value("POSTGRES_OUTPUT_HOST"),
        postgres_port=config_manager.get_value("POSTGRES_OUTPUT_PORT"),
        postgres_db=config_manager.get_value("POSTGRES_OUTPUT_DB"),
        postgres_user=config_manager.get_value("POSTGRES_OUTPUT_USER"),
        postgres_password=config_manager.get_value("POSTGRES_OUTPUT_PASSWORD"),
        schema_host=config_manager.get_value("SCHEMA_HOST"),
        schema_port=config_manager.get_value("SCHEMA_PORT"),
        kafka_host=config_manager.get_value("KAFKA_HOST"),
        kafka_port=config_manager.get_value("KAFKA_PORT")
    )

    send_config_to_kafka_connect(postgres_sink, host=config_manager.get_value("KAFKA_CONNECT_HOST"),
                                 port=config_manager.get_value("KAFKA_CONNECT_PORT"))
    send_config_to_kafka_connect(postgres_source, host=config_manager.get_value("KAFKA_CONNECT_HOST"),
                                 port=config_manager.get_value("KAFKA_CONNECT_PORT"))


