# pylint: skip-file

import pytest
from unittest.mock import patch, MagicMock

from extract_short import get_object_name, get_plant_data, get_recording_info, extract_recordings


def test_get_object_name():
    result = get_object_name()

    assert isinstance(result, str)
    assert result.startswith('recording-')
    assert result.endswith('.json')


@patch('requests.get')
def test_get_plant_data(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "plant_id": 1,
        "soil_moisture": "25.5",
        "temperature": "22.3",
        "last_watered": "2024-10-01"
    }
    mock_get.return_value = mock_response

    result = get_plant_data(1)

    assert len(result) == 1
    assert isinstance(result, list)
    assert isinstance(result[0], dict)


@pytest.mark.parametrize("reading_data, expected", [
    (
        {"plant_id": 1, "botanist": {"name": "Jane Doe"}, "recording_taken": "2024-10-01T10:00:00Z",
            "soil_moisture": "30.5", "temperature": "22.5", "last_watered": "2024-09-30"},
        {"plant_id": 1, "botanist_name": "Jane Doe", "at": "2024-10-01T10:00:00Z",
            "soil_moisture": 30.5, "temperature": 22.5, "last_watered": "2024-09-30"}
    ),
    ({"error": "Not found"}, None),
    ({"plant_id": 3, "botanist": {"name": None}, "recording_taken": "2024-10-01T10:00:00Z", "soil_moisture": "0", "temperature": "-10", "last_watered": "2024-09-30"},
     {"plant_id": 3, "botanist_name": None, "at": "2024-10-01T10:00:00Z", "soil_moisture": 0.0, "temperature": -10.0, "last_watered": "2024-09-30"}),
])
def test_get_recording_info(reading_data, expected):
    assert get_recording_info(reading_data) == expected


@patch('json.dump')
@patch('builtins.open', new_callable=MagicMock)
@patch('extract_short.get_object_name')
@patch('extract_short.get_recording_info')
@patch('extract_short.get_plant_data')
def test_extract_recordings(mock_get_plant_data, mock_get_recording_info, mock_get_object_name, mock_open, mock_json_dump):

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "plant_id": 1,
        "soil_moisture": "25.5",
        "temperature": "22.3",
        "last_watered": "2024-10-01",
        "recording_taken": "2024-10-01"
    }

    mock_get_plant_data.return_value = [mock_response]
    mock_get_recording_info.return_value = {
        "plant_id": 1,
        "botanist_name": "Jane Doe",
        "at": "2024-10-01T10:00:00Z",
        "soil_moisture": 25.5,
        "temperature": 22.3,
        "last_watered": "2024-10-01"
    }

    # Control the output of get_object_name
    mock_get_object_name.return_value = "recording-2024-10-02-15-30.json"

    object_name = extract_recordings()

    assert object_name == "recording-2024-10-02-15-30.json"
    mock_open.assert_called_once_with(object_name, "w", encoding='UTF-8')
    mock_json_dump.assert_called_once()
