# pylint: skip-file

# test_transform_long.py
import pytest
import pandas as pd
from transform_long import create_summary


class TestCreateSummary:

    @pytest.mark.parametrize("input_data, expected_data", [
        (
            pd.DataFrame({
                "plant_id": [1, 1, 1],
                "plant_name": ["Rose", "Rose", "Rose"],
                "temperature": [22.1234, 25.4567, 20.9876],
                "soil_moisture": [30.5123, 35.6789, 28.2345],
                "last_watered": ["2024-09-29", "2024-09-29", "2024-09-29"]
            }),
            pd.DataFrame({
                "plant_id": [1],
                "plant_name": ["Rose"],
                "min_T": [20.9876],
                "max_T": [25.4567],
                "min_M": [28.2345],
                "max_M": [35.6789],
                "water_count": [1],
                "std_T": [2.3228],
                "std_M": [3.8145]
            })
        ),
        (
            pd.DataFrame({
                "plant_id": [1, 2],
                "plant_name": ["Rose", "Tulip"],
                "temperature": [22.1234, 15.5678],
                "soil_moisture": [30.5123, 25.6789],
                "last_watered": ["2024-09-29", "2024-09-28"]
            }),
            pd.DataFrame({
                "plant_id": [1, 2],
                "plant_name": ["Rose", "Tulip"],
                "min_T": [22.1234, 15.5678],
                "max_T": [22.1234, 15.5678],
                "min_M": [30.5123, 25.6789],
                "max_M": [30.5123, 25.6789],
                "water_count": [1, 1],
                "std_T": [None, None],
                "std_M": [None, None]
            })
        )
    ])
    def test_input(self, input_data, expected_data):
        result = create_summary(input_data, 4)

        expected_data = expected_data.fillna('N/A')
        result = result.fillna('N/A')

        pd.testing.assert_frame_equal(result.reset_index(
            drop=True), expected_data.reset_index(drop=True))

    def test_empty(self):

        input_data = pd.DataFrame(
            columns=["plant_id", "plant_name", "temperature", "soil_moisture", "last_watered"])
        result = create_summary(input_data)

        columns = ["plant_id", "plant_name", "min_T", "max_T",
                   "min_M", "max_M", "water_count", "std_T", "std_M"]

        assert len(result.index) == 0
        for column in result.columns:
            assert column in columns
