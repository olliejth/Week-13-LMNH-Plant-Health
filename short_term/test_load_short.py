# pylint: skip-file

import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from load_short import convert_at_datetime, convert_last_watered_datetime, format_reading_tuples, upload_readings


class TestLoadShort(unittest.TestCase):

    def test_convert_at_datetime(self):
        date_str = "2024-10-01 12:30:45"
        expected = datetime(2024, 10, 1, 12, 30, 45)
        result = convert_at_datetime(date_str)
        self.assertEqual(result, expected)

    def test_convert_last_watered_datetime(self):
        date_str = "Mon, 01 Oct 2024 12:30:45 GMT"
        expected = datetime(2024, 10, 1, 12, 30, 45)
        result = convert_last_watered_datetime(date_str)
        self.assertEqual(result, expected)

    def test_format_reading_tuples(self):
        data = [
            (1, 101, "2024-10-01 12:30:45", "30.5",
             "22.5", "Mon, 01 Oct 2024 12:30:45 GMT"),
            (2, 102, "2024-10-02 11:30:45", "25.0",
             "21.0", "Sun, 30 Sep 2024 12:30:45 GMT")
        ]
        expected = [
            (1, 101, datetime(2024, 10, 1, 12, 30, 45), "30.5",
             "22.5", datetime(2024, 10, 1, 12, 30, 45)),
            (2, 102, datetime(2024, 10, 2, 11, 30, 45), "25.0",
             "21.0", datetime(2024, 9, 30, 12, 30, 45)),
        ]
        result = format_reading_tuples(data)
        self.assertEqual(result, expected)

    @patch('load_short.get_connection')
    @patch('load_short.get_plant_ids')
    def test_upload_readings(self, mock_get_plant_ids, mock_get_connection):
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

        self.assertEqual(mock_cursor.execute.call_count, 2)

        expected_query = """INSERT INTO beta.reading (plant_id, botanist_id,
        at, soil_moisture, temperature, last_watered) VALUES """
        self.assertIn(expected_query,
                      mock_cursor.execute.call_args_list[0][0][0])
