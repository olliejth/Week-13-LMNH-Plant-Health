from unittest.mock import patch, MagicMock

import pytest

import pandas as pd
import altair as alt
import pytest

from longterm_transform import concat_csvs, get_times_watered, get_max_temp_per_plant, get_min_moisture_per_plant


@pytest.fixture
def sample_df():
    data = {
        'plant_id': [1, 1, 2, 2, 3],
        'water_count': [3, 2, 5, 6, 4],
        'max_T': [30, 32, 28, 35, 29],
        'min_M': [50, 45, 52, 40, 48]
    }
    return pd.DataFrame(data)


@pytest.mark.parametrize("files, dfs, expected_df", [
    (["file1.csv", "file2.csv", "file3.csv"],
     {"file1.csv": pd.DataFrame({'plant_id': [1, 1], 'water_count': [3, 2]}),
      "file2.csv": pd.DataFrame({'plant_id': [2, 2], 'water_count': [5, 6]}),
      "file3.csv": pd.DataFrame({'plant_id': [3], 'water_count': [4]})},
     pd.DataFrame({'plant_id': [1, 1, 2, 2, 3], 'water_count': [3, 2, 5, 6, 4]})),
    (["file1.csv"], {"file1.csv": pd.DataFrame({'plant_id': [1, 1], 'water_count': [3, 2]})},
     pd.DataFrame({'plant_id': [1, 1], 'water_count': [3, 2]})),
    (["file2.csv", "file3.csv"],
     {"file2.csv": pd.DataFrame({'plant_id': [2, 2], 'water_count': [5, 6]}),
      "file3.csv": pd.DataFrame({'plant_id': [3], 'water_count': [4]})},
     pd.DataFrame({'plant_id': [2, 2, 3], 'water_count': [5, 6, 4]}))])
@patch('pandas.read_csv')
def test_concat_csvs(mock_read_csv, files, dfs, expected_df):
    mock_read_csv.side_effect = lambda file: dfs[file]

    result_df = concat_csvs(files)
    print(result_df)

    pd.testing.assert_frame_equal(result_df, expected_df)


def test_get_times_watered(sample_df):
    result_chart = get_times_watered(sample_df)

    assert isinstance(result_chart, alt.Chart)
    assert result_chart.mark.type == 'bar'


def test_get_max_temp_per_plant(sample_df):
    result_chart = get_max_temp_per_plant(sample_df)

    assert isinstance(result_chart, alt.Chart)
    assert result_chart.mark.type == 'bar'


def test_get_min_moisture_per_plant(sample_df):

    result_chart = get_min_moisture_per_plant(sample_df)

    assert isinstance(result_chart, alt.Chart)
    assert result_chart.mark.type == 'bar'
