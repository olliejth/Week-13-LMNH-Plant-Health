# pylint: skip-file
from unittest.mock import patch
from extract import extract_botanist_data, extract_location_data, extract_plant_data


class TestExtract:

    def test_get_botanist_data(self):

        raw_data = {
            "email": "eliza.andrews@lnhm.co.uk",
            "name": "Eliza Andrews",
            "phone": "(846)669-6651x75948"
        }

        data = extract_botanist_data(raw_data)

        assert data["first_name"] == "Eliza"
        assert data["last_name"] == "Andrews"
        assert data["email"] == "eliza.andrews@lnhm.co.uk"
        assert data["phone"] == "(846)669-6651x75948"

    def test_get_botanist_data_middle_name(self):

        raw_data = {
            "email": "john@example.com",
            "name": "First Middle Last",
            "phone": "12345678"
        }

        data = extract_botanist_data(raw_data)

        assert data["first_name"] == "First"
        assert data["last_name"] == "Last"
        assert data["email"] == "john@example.com"
        assert data["phone"] == "12345678"

    @patch("extract.get_timezone_from_region")
    def test_extract_location_data(self, fake_tz):

        fake_tz.return_value = "GMT"

        raw_data = [
            "33.95015",
            "-118.03917",
            "South Whittier",
            "US",
            "Somewhere"
        ]
        data = extract_location_data(raw_data)
        assert data["latitude"] == 33.95015
        assert data["longitude"] == -118.03917
        assert data["town"] == "South Whittier"
        assert data["timezone"] == "GMT"
