# pylint: skip-file
from extract import get_botanist_data


class TestExtract:

    def test_get_botanist_data(self):

        raw_data = {
            "email": "eliza.andrews@lnhm.co.uk",
            "name": "Eliza Andrews",
            "phone": "(846)669-6651x75948"
        }

        data = get_botanist_data(raw_data)

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

        data = get_botanist_data(raw_data)

        assert data["first_name"] == "First"
        assert data["last_name"] == "Last"
        assert data["email"] == "john@example.com"
        assert data["phone"] == "12345678"
