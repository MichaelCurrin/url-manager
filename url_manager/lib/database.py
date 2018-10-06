"""
Database initialisation and storage handling module.

See docs for setting up the database.

Usage:
    $ python -m lib.database [args]
"""
import models
from lib.config import AppConf

# Make model objects available on the lib.database module.
from models import *
from models.connection import conn


conf = AppConf()


def initialize(drop_all=False, create_all=True):
    """
    Initialize the tables in the database.

    Gets class objects from the imported list of names. By default, no tables
    are dropped and all tables are created or skipped.

    @param dropAll: Default False. If set to True, drop all tables before
        creating them.
    @param createAll: Default True. Iterate through table names and create
        the tables which they do not exist yet.

    @return: Count of table models in the available list.
    """
    models_list = []

    for table_name in models.__all__:
        table_class = getattr(models, table_name)
        models_list.append(table_class)

    if drop_all:
        for m in models_list:
            print("Dropping {0}".format(m.__name__))
            m.dropTable(ifExists=True, cascade=True)

    if create_all:
        for m in models_list:
            print("Creating {0}".format(m.__name__))
            m.createTable(ifNotExists=True)

    return len(models_list)


def main():
    print("Database path: {0}".format(conf.get('db', 'path')))
    print("Deleting all tables for develop mode, then creating tables.")
    c = initialize(drop_all=True, create_all=True)
    print("Count of tables: now {}.\n".format(c))


if __name__ == '__main__':
    main()
