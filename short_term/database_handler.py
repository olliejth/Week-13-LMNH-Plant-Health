"""Script to handle the connections and querying of the SQL server db."""


from os import environ as ENV

from pymssql import connect
from dotenv import load_dotenv


def get_connection(dict_handler: bool = True):
    """Returns a database connection."""
    return connect(
        server=ENV['DB_HOST'],
        port=ENV['DB_PORT'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        database=ENV['DB_NAME'],
        as_dict=dict_handler
    )
