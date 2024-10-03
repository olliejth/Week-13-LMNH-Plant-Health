"""Extracts all reading data from the short-term database."""

from os import environ as ENV

import pandas as pd
from pymssql import connect  # pylint: disable=E0611
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Establishes and returns a pymssql connection to the database."""

    connection = connect(
        server=ENV['DB_HOST'],
        port=ENV['DB_PORT'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        database=ENV['DB_NAME']
    )

    return connection


def extract_readings():
    """Extracts all readings from the 'reading' table and returns a pandas DataFrame."""

    with get_db_connection() as connection:
        schema_name = ENV['SCHEMA_NAME']

        query = f'''
        SELECT plant_id, botanist_id, at, last_watered,
          soil_moisture, temperature FROM {schema_name}.reading
        '''

        df = pd.read_sql(query, connection)

        return df


if __name__ == "__main__":

    my_df = extract_readings()
