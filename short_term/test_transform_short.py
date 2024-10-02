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


def test_format_tuple(mock_botanist_details):

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


@patch.dict('os.environ', {
    'DB_HOST': 'dummy_host',
    'DB_PORT': 'dummy_port',
    'DB_USER': 'dummy_user',
    'DB_PASSWORD': 'dummy_password',
    'DB_NAME': 'dummy_db',
    'SCHEMA_NAME': 'dummy_schema'
})
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
@patch('pymssql.connect')
def test_transform_recordings(mock_connect, mock_get_botanist_ids, mock_open):

    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

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
    mock_connect.assert_called_once()
