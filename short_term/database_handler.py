"""Script to handle the connections and querying of the SQL server db."""


from os import environ as ENV

from pymssql import connect
from dotenv import load_dotenv
