# pylint: skip-file

import pandas as pd
import altair as alt
from unittest.mock import patch, MagicMock
import pytest

from transform_dashboard import get_botanist_mapping, create_botanist_pie, create_temperature_bar, create_temperature_line, create_moisture_bar


@patch.dict('os.environ', {'DB_HOST': 'fake_host',
                           'DB_PORT': '5432',
                           'DB_USER': 'fake_user',
                           'DB_PASSWORD': 'fake_password',
                           'DB_NAME': 'fake_db',
                           'SCHEMA_NAME': 'fake_schema'})
@patch('transform_dashboard.get_db_connection')
@patch('pandas.read_sql')
def test_get_botanist_mapping(mock_read_sql, mock_get_db_connection):

    mock_conn = MagicMock()
    mock_get_db_connection.return_value.__enter__.return_value = mock_conn
    fake_df = pd.DataFrame({
        'botanist_id': [1, 2],
        'first_name': ['John', 'Jane'],
        'last_name': ['Doe', 'Smith']
    })
    mock_read_sql.return_value = fake_df

    result = get_botanist_mapping()
    expected = {1: 'John Doe', 2: 'Jane Smith'}

    mock_read_sql.assert_called_once_with(f'''
        SELECT botanist_id, first_name, last_name FROM fake_schema.botanist
        ''', mock_conn)
    assert result == expected


@patch.dict('os.environ', {'DB_HOST': 'fake_host',
                           'DB_PORT': '5432',
                           'DB_USER': 'fake_user',
                           'DB_PASSWORD': 'fake_password',
                           'DB_NAME': 'fake_db',
                           'SCHEMA_NAME': 'fake_schema'})
@patch('transform_dashboard.get_botanist_mapping')
def test_create_botanist_pie(mock_get_botanist_mapping):
    df = pd.DataFrame(columns=['botanist_id', 'plant_id'])

    result_chart = create_botanist_pie(df)

    assert isinstance(result_chart, alt.Chart)
    assert result_chart.mark == 'arc'


def test_create_temperature_bar():
    df = pd.DataFrame(columns=['plant_id', 'temperature', 'at'])

    result_chart = create_temperature_bar(df)

    assert isinstance(result_chart, alt.Chart)
    assert result_chart.mark == 'bar'


def test_create_temperature_line():
    df = pd.DataFrame(columns=['plant_id', 'temperature', 'at'])

    result_chart = create_temperature_line(df)

    assert isinstance(result_chart, alt.Chart)
    assert result_chart.mark == 'line'


def test_create_moisture_bar():
    df = pd.DataFrame(columns=['plant_id', 'soil_moisture', 'at'])

    result_chart = create_moisture_bar(df)

    assert isinstance(result_chart, alt.Chart)
    assert result_chart.mark == 'bar'
