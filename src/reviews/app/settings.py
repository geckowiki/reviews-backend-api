import os
from enum import Enum
from re import M


class DBDriver(str, Enum):
    SYNC = "postgresql+psycopg2"
    ASYNC = "postgresql+asyncpg"


class Settings:
    SECRET_KEY = "iva-t7oyv1rdk#e6()#wvve7*3q3par26(7u3n(ne1sr*4ht@a"

    def get_database_url(self, db_driver: DBDriver = DBDriver.SYNC) -> str:
        return "{db_driver}://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}".format(
            db_driver=db_driver,
            db_username=os.getenv("DB_USERNAME"),
            db_password=os.getenv("DB_PASSWORD"),
            db_hostname=os.getenv("DB_HOSTNAME"),
            db_port=os.getenv("DB_PORT"),
            db_name=os.getenv("DB_NAME"),
        )


settings = Settings()
