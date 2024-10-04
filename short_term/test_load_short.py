# pylint: skip-file

from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest

from load_short import convert_at_datetime, convert_last_watered_datetime, format_reading_tuples, upload_readings


@pytest.mark.parametrize("date_str, expected", [
    ("2024-10-01 12:30:45", datetime(2024, 10, 1, 12, 30, 45)),
    ("2024-12-31 23:59:59", datetime(2024, 12, 31, 23, 59, 59)),
    ("2023-01-01 00:00:00", datetime(2023, 1, 1, 0, 0, 0)),
])
def test_convert_at_datetime(date_str, expected):
    result = convert_at_datetime(date_str)
    assert result == expected


@pytest.mark.parametrize("date_str, expected", [
    ("Mon, 01 Oct 2024 12:30:45 GMT", datetime(2024, 10, 1, 12, 30, 45)),
    ("Fri, 31 Dec 2023 23:59:59 GMT", datetime(2023, 12, 31, 23, 59, 59)),
    ("Sun, 01 Jan 2023 00:00:00 GMT", datetime(2023, 1, 1, 0, 0, 0)),
])
def test_convert_last_watered_datetime(date_str, expected):
    result = convert_last_watered_datetime(date_str)
    assert result == expected


@patch('load_short.convert_at_datetime')
@patch('load_short.convert_last_watered_datetime')
def test_format_reading_tuples_output_types(mock_convert_last_watered_datetime, mock_convert_at_datetime):
    data = [
        (1, 101, "2024-10-01 12:30:45", "30.5",
         "22.5", "Mon, 01 Oct 2024 12:30:45 GMT"),
        (2, 102, "2024-10-02 11:30:45", "25.0",
         "21.0", "Sun, 30 Sep 2024 12:30:45 GMT"),
    ]

    mock_convert_at_datetime.return_value = datetime(2024, 10, 1, 12, 30, 45)
    mock_convert_last_watered_datetime.return_value = datetime(
        2024, 10, 1, 12, 30, 45)

    result = format_reading_tuples(data)

    for reading in result:
        assert isinstance(reading[0], int)  # plant_id
        assert isinstance(reading[1], int)  # botanist_id
        assert isinstance(reading[2], datetime)  # at
        assert isinstance(reading[3], str)  # soil_moisture
        assert isinstance(reading[4], str)  # temperature
        assert isinstance(reading[5], datetime)  # last_watered


@patch('load_short.get_connection')
@patch('load_short.get_plant_ids')
def test_upload_readings(mock_get_plant_ids, mock_get_connection):
    mock_get_plant_ids.return_value = [1, 2]

    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    tuples = [
        (1, 101, "2024-10-01 12:30:45", "30.5",
         "22.5", "Mon, 01 Oct 2024 12:30:45 GMT"),
        (2, 102, "2024-10-02 11:30:45", "25.0",
         "21.0", "Sun, 30 Sep 2024 12:30:45 GMT"),
        (3, 103, "2024-10-03 10:30:45", "40.0", "24.0",
         "Sat, 29 Sep 2024 12:30:45 GMT"),
    ]

    upload_readings(tuples)

    assert mock_cursor.execute.call_count == 1

    expected_query = """INSERT INTO beta.reading (plant_id, botanist_id,
    at, soil_moisture, temperature, last_watered) VALUES ( %s, %s, %s, %s, %s, %s )"""
    assert expected_query in mock_cursor.execute.call_args_list[0][0][0]
