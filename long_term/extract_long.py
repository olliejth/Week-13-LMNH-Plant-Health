"""Extracts all reading data from database between 24 and 48 hours old."""

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

        query = f'''
        SELECT plant_id, at, last_watered, soil_moisture, 
        temperature FROM {ENV['SCHEMA_NAME']}.reading
        WHERE at BETWEEN DATEADD(hour, -48, SYSDATETIME()) AND DATEADD(hour, -24, SYSDATETIME())
        '''

        df = pd.read_sql(query, connection)
        print(f'Extracted {len(df.index)} rows')
        return df


if __name__ == '__main__':
    df_readings = extract_readings()
    print(df_readings.head())
