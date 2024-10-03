"""Script to handle the connections and querying of the SQL server db."""


from os import environ as ENV

from pymssql import connect  # pylint: disable=E0611
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Returns a database connection."""
    return connect(
        server=ENV['DB_HOST'],
        port=ENV['DB_PORT'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        database=ENV['DB_NAME'],
        as_dict=True
    )


def get_plant_ids() -> list[int]:
    """Returns a list of all plants in the database."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT plant_id FROM beta.plant;")
            plant_ids = cursor.fetchall()
            return [x['plant_id'] for x in plant_ids]


def get_botanist_ids() -> dict:
    """Returns a dictionary mapping botanist names to IDs."""
    query_str = """
        SELECT botanist_id, first_name, last_name 
        FROM beta.botanist;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_str)
            result = cursor.fetchall()

    botanist_dict = {
        f"{row['first_name']} {row['last_name']}": row['botanist_id']
        for row in result
    }
    return botanist_dict
