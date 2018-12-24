"""
Connection module.
"""
from sqlobject.sqlite import builder

from lib.config import AppConf


def setup_connection():
    """
    Create connection to a database using configured file path.

    The SQLite DB file will be created if it does not exist.

    :return conn: Database connection object. This must be included in each
        model class for it to have access to the DB.
    """
    db_path = AppConf().get('db', 'path')
    conn = builder()(db_path)

    return conn


conn = setup_connection()
