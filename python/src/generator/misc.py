from fkbutils.dbwrapper import PostgresWrapper
from fkbutils.misc import ConfigManager


def get_postgres_wrapper(config_manager: ConfigManager):
    return PostgresWrapper(host=config_manager.get_value("POSTGRES_INPUT_HOST"),
                           port=config_manager.get_value("POSTGRES_INPUT_PORT"),
                           user=config_manager.get_value("POSTGRES_INPUT_USER"),
                           password=config_manager.get_value("POSTGRES_INPUT_PASSWORD"),
                           dbname=config_manager.get_value("POSTGRES_INPUT_DB"),
                           )