# pylint: skip-file

# test_transform_long.py
from unittest.mock import patch

import pytest
import pandas as pd

from transform_long import create_summary, round_numerical_columns


@pytest.mark.parametrize("input_data, columns, round_dp, expected_output", [
    (pd.DataFrame({"A": [1.1234, 2.5678, None], "B": [3.1415, None, 2.7182]}), ["A", "B"], 2,
     pd.DataFrame({"A": [1.12, 2.57, None], "B": [3.14, None, 2.72]})),
    (pd.DataFrame({"A": [1.1234, 2.5678, 3.8765], "B": [3.1415, 2.7182, 1.4142]}), ["A"], 1,
     pd.DataFrame({"A": [1.1, 2.6, 3.9], "B": [3.1415, 2.7182, 1.4142]})),
    (pd.DataFrame({"A": [None, None, None], "B": [None, None, None]}), ["A", "B"], 2,
     pd.DataFrame({"A": [None, None, None], "B": [None, None, None]})),
    (pd.DataFrame({"A": [0.0001, 0.0002, 0.0003], "B": [0.9999, 0.8888, 0.7777]}), ["A", "B"], 4,
     pd.DataFrame({"A": [0.0001, 0.0002, 0.0003], "B": [0.9999, 0.8888, 0.7777]})),
    (pd.DataFrame({"A": [-1.1234, -2.5678, None], "B": [3.1415, None, -2.7182]}), ["A", "B"], 2,
     pd.DataFrame({"A": [-1.12, -2.57, None], "B": [3.14, None, -2.72]})),
    (pd.DataFrame({"A": [1.5, 2.5, 3.5], "B": [1.5, 2.5, 3.5]}), ["A", "B"], 0,
     pd.DataFrame({"A": [2.0, 2.0, 4.0], "B": [2.0, 2.0, 4.0]})),
    (pd.DataFrame({"A": [float('inf'), float('-inf'), float('nan')], "B": [3.1415, -2.7182, 0.0]}), ["A", "B"], 2,
     pd.DataFrame({"A": [float('inf'), float('-inf'), None], "B": [3.14, -2.72, 0.0]})),
    (pd.DataFrame({"A": [1, 2, 3]}), ["A"], 1, pd.DataFrame({"A": [1, 2, 3]})),
])
def test_round_numerical_columns(input_data, columns, round_dp, expected_output):
    result = round_numerical_columns(input_data, columns, round_dp)
    result = result.fillna('N/A')
    expected_output = expected_output.fillna('N/A')

    print(result, expected_output)
    pd.testing.assert_frame_equal(result, expected_output)


class TestCreateSummary:

    @pytest.mark.parametrize("input_data, expected_data", [
        (
            pd.DataFrame({
                "plant_id": [1, 1, 1],
                "temperature": [22.1234, 25.4567, 20.9876],
                "soil_moisture": [30.5123, 35.6789, 28.2345],
                "last_watered": ["2024-09-29", "2024-09-29", "2024-09-29"]
            }),
            pd.DataFrame({
                "plant_id": [1],
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
                "temperature": [22.1234, 15.5678],
                "soil_moisture": [30.5123, 25.6789],
                "last_watered": ["2024-09-29", "2024-09-28"]
            }),
            pd.DataFrame({
                "plant_id": [1, 2],
                "min_T": [22.1234, 15.5678],
                "max_T": [22.1234, 15.5678],
                "min_M": [30.5123, 25.6789],
                "max_M": [30.5123, 25.6789],
                "water_count": [1, 1],
                "std_T": [None, None],
                "std_M": [None, None]
            })
        ),
        (
            pd.DataFrame({
                "plant_id": [1, 1, 1],
                "temperature": [None, None, None],
                "soil_moisture": [None, None, None],
                "last_watered": [None, None, None]
            }),
            pd.DataFrame({
                "plant_id": [1],
                "min_T": ["N/A"],
                "max_T": ["N/A"],
                "min_M": ["N/A"],
                "max_M": ["N/A"],
                "water_count": [0],
                "std_T": ["N/A"],
                "std_M": ["N/A"]
            })
        )
    ])
    @patch('transform_long.round_numerical_columns')
    def test_input(self, mock_round, input_data, expected_data):

        mock_round.side_effect = lambda df, cols, dp: df
        expected_data = expected_data.fillna('N/A')

        result = create_summary(input_data, 4)
        result['std_T'] = result['std_T'].apply(
            lambda x: round(x, 4) if not pd.isna(x) else None)
        result['std_M'] = result['std_M'].apply(
            lambda x: round(x, 4) if not pd.isna(x) else None)
        result = result.fillna('N/A')

        pd.testing.assert_frame_equal(result, expected_data, check_dtype=False)

    @patch('transform_long.round_numerical_columns')
    def test_empty(self, mock_round):

        input_data = pd.DataFrame(
            columns=["plant_id", "plant_name", "temperature", "soil_moisture", "last_watered"])

        result = create_summary(input_data)

        columns = ["plant_id", "plant_name", "min_T", "max_T",
                   "min_M", "max_M", "water_count", "std_T", "std_M"]

        assert len(result.index) == 0
        for column in result.columns:
            assert column in columns
