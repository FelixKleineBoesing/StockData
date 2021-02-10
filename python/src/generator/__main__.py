from pathlib import Path

from fkbutils.misc import ConfigManager

from src.generator import get_default_variables
from src.generator.__main__initialization import import_init_dataset
from src.generator.generator import generate_new_prices
from src.misc.helpers import get_postgres_wrapper


def main():
    postgres = get_postgres_wrapper(
        ConfigManager(
            default_variables=get_default_variables(),
            env_file=Path("../../.env")
        )
    )
    import_init_dataset(postgres)
    generate_new_prices(postgres=postgres)


if __name__ == "__main__":
    main()