# pylint: skip-file

from unittest.mock import patch, mock_open

import pytest

from transform_short import format_tuple, transform_recordings


@pytest.fixture
def mock_botanist_details():
    """Mock botanist details for testing."""
    return {
        "Jane Doe": 101,
        "John Smith": 102
    }


def test_format_tuple(mock_botanist_details):
    """Test the format_tuple function."""
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


@patch('builtins.open', new_callable=mock_open, read_data='''[
    {
        "plant_id": 1,
        "botanist_name": "Jane Doe",
        "at": "2024-10-01T10:00:00Z",
        "soil_moisture": "30.5",
        "temperature": "22.5",
        "last_watered": "2024-09-30"
    },
    {
        "plant_id": 2,
        "botanist_name": "John Smith",
        "at": "2024-10-01T10:00:00Z",
        "soil_moisture": "25.0",
        "temperature": "21.0",
        "last_watered": "2024-09-29"
    }]''')
@patch('database_handler.get_botanist_ids')
def test_transform_recordings(mock_get_botanist_ids, mock_open):
    """Test the transform_recordings function."""
    mock_get_botanist_ids.return_value = {
        "Jane Doe": 101,
        "John Smith": 102
    }

    expected_output = [
        (1, 101, "2024-10-01T10:00:00Z", "30.5", "22.5", "2024-09-30"),
        (2, 102, "2024-10-01T10:00:00Z", "25.0", "21.0", "2024-09-29")
    ]

    result = transform_recordings('dummy_file.json')

    assert result == expected_output
    mock_open.assert_called_once_with('dummy_file.json', 'r', encoding='UTF-8')
    mock_get_botanist_ids.assert_called_once()
