# pylint: skip-file

import pandas as pd
import altair as alt
from unittest.mock import patch, MagicMock
import pytest

from transform_dashboard import get_botanist_mapping, create_botanist_pie, create_temperature_bar, create_temperature_line, create_moisture_bar


@patch('transform_dashboard.get_db_connection')
def test_get_botanist_mapping(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_get_db_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value.fetchall.return_value = [
        (1, 'John', 'Doe'), (2, 'Jane', 'Smith')]

    result = get_botanist_mapping()

    expected = {1: 'John Doe', 2: 'Jane Smith'}
    assert result == expected
    mock_conn.execute.assert_called_once()


def test_create_botanist_pie():
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
