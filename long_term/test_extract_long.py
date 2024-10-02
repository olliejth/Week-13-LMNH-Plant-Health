# pylint: skip-file

from os import environ as ENV
from unittest.mock import patch, MagicMock

import pandas as pd


from extract_long import extract_readings


class TestExtractReadings():

    @patch.dict(ENV, {'SCHEMA_NAME': 'dummy_schema'})
    @patch('pandas.read_sql')
    @patch('extract_long.get_db_connection')
    def test_calls(self, mock_get_db_connection, mock_read_sql):
        mock_connection = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_connection

        mock_read_sql.return_value = pd.DataFrame({})

        extract_readings()

        mock_get_db_connection.assert_called_once()
        mock_read_sql.assert_called_once()

    @patch.dict(ENV, {'SCHEMA_NAME': 'dummy_schema'})
    @patch('pandas.read_sql')
    @patch('extract_long.get_db_connection')
    def test_with_data(self, mock_get_db_connection, mock_read_sql):
        mock_connection = MagicMock()
        mock_get_db_connection.return_value.__enter__.return_value = mock_connection

        dummy_data = {
            'plant_id': [1, 2],
            'at': ['2024-10-01 12:00:00', '2024-10-01 13:00:00'],
            'last_watered': ['2024-09-29', '2024-09-29'],
            'soil_moisture': [30.5, 45.2],
            'temperature': [22.0, 25.5]
        }
        mock_read_sql.return_value = pd.DataFrame(dummy_data)

        df = extract_readings()

        assert len(df) == 2
        pd.testing.assert_frame_equal(df, pd.DataFrame(dummy_data))
