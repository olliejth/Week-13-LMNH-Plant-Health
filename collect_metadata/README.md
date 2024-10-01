# Collecting Metadata
This folder contains an ETL script that sends the plant metadata to the S3 bucket.

## Setup
- Using a `venv`, or otherwise, run `pip install -r requirements.txt`.
- Run `python3 transform.py`.
- You should have the 3 metadata `csv` files generated in the directory.

## Files Explained
- `extract.py`: Extracts the plant data from the API.
- `transform.py`: Transforms the metadata into `csv` files.
- `test_main.py`: Tests the scripts.