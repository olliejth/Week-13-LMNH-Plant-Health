# pylint: skip-file

"""Test file for load functions."""

from unittest.mock import patch, MagicMock
from datetime import date

import pytest
import pandas as pd

from load_long import create_csv, get_s3_client, upload_csv, load_recordings


class TestCreateCSV():

    @patch("pandas.DataFrame.to_csv")
    def test_create_csv_core_functionality(self, mock_to_csv):

        mock_df = pd.DataFrame({"c1": [1, 2], "c2": [3, 4]})

        expected_filename = f"summary-{date.today()}.csv"

        assert create_csv(mock_df) == expected_filename

    @patch("pandas.DataFrame.to_csv")
    def test_create_csv_calls_to_csv(self, mock_to_csv):

        mock_df = pd.DataFrame({"c1": [1, 2], "c2": [3, 4]})

        res = create_csv(mock_df)

        mock_to_csv.assert_called_once_with(res, index=False)

    @patch("pandas.DataFrame.to_csv")
    def test_create_csv_error_on_invlaid_input(self, mock_to_csv):

        mock_df = "string"

        with pytest.raises(TypeError) as err:
            create_csv(mock_df)

        assert err.value.args[0] == "Invalid data, input data must be a pandas dataframe."


class TestGetS3Client():

    @patch.dict("load_long.ENV", {"AWS_rvbyaulf_KEY": "test_access_key", "AWS_rvbyaulf_SECRET_KEY": "test_secret_key"})
    @patch("load_long.client")
    def test_get_s3_client_core_functionality(self, mock_s3_client):

        get_s3_client()

        mock_s3_client.assert_called_once_with(
            service_name="s3",
            aws_access_key_id="test_access_key",
            aws_secret_access_key="test_secret_key"
        )


class TestUploadCSV():

    # Mock the environment variable
    @patch('load_long.ENV', {"BUCKET_NAME": "test-bucket"})
    @patch('load_long.client')
    def test_upload_csv(self, mock_s3_client):
        mock_s3_client.upload_file = MagicMock()

        upload_csv("test_file.csv", mock_s3_client)

        mock_s3_client.upload_file.assert_called_once_with(
            "test_file.csv",
            "test-bucket",
            "recordings/test_file.csv"
        )
