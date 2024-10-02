# pylint: skip-file

from unittest.mock import patch, mock_open, MagicMock

import pytest

from transform_short import format_tuple, transform_recordings


@pytest.fixture
def mock_botanist_details():
    return {
        "Jane Doe": 101,
        "John Smith": 102
    }


def test_format_tuple_data_type(mock_botanist_details):

    reading_data = {
        "plant_id": 1,
        "botanist_name": "Jane Doe",
        "at": "2024-10-01T10:00:00Z",
        "soil_moisture": 30.5,
        "temperature": 22.5,
        "last_watered": "2024-09-30"
    }
    result = format_tuple(reading_data, mock_botanist_details)

    assert isinstance(result, tuple)
    assert isinstance(result[0], int)
    assert isinstance(result[1], str)
    assert isinstance(result[3], str)


def test_format_tuple_with_input(mock_botanist_details):

    reading_data = {
        "plant_id": 1,
        "botanist_name": "Jane Doe",
        "at": "2024-10-01T10:00:00Z",
        "soil_moisture": "30.5",
        "temperature": "22.5",
        "last_watered": "2024-09-30"
    }

    expected_output = (1, 101, "2024-10-01T10:00:00Z",
                       "30.5", "22.5", "2024-09-30")
    result = format_tuple(reading_data, mock_botanist_details)

    assert result == expected_output
