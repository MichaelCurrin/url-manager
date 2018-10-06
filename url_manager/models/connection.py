# -*- coding: utf-8 -*-
"""
Connection module.

Setup a connection to the database.
"""
from sqlobject.sqlite import builder

from lib.config import AppConf


def setup_connection():
    """
    Create connection to a database.

    The SQLite db file will be created if it does not exist.

    @return conn: Database connection object. This must included in each
        model class.
    """
    db_path = AppConf().get('db', 'path')
    conn = builder()(db_path)

    return conn


conn = setup_connection()
