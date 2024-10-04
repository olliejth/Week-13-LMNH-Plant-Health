# 🚀 Short Term ETL Pipeline

This folder contains scripts to **asynchronously query the LMNH plants API**, transform and clean the data, and upload it to the **AWS RDS** instance. The ETL pipeline is part of a broader effort to monitor plant health in real-time by collecting, processing, and storing data efficiently.

---

## 🛠️ Prerequisites

Ensure that you have the following:
- **Docker** installed for containerisation.
- **AWS CLI** configured to interact with AWS services (ECR, Lambda, RDS, etc.)
- **Python** installed on your local machine. 
---

## 📂 Setup

Please ensure you have a `.env` file with the following environment variables before starting:

```bash
DB_HOST=XXXXXX
DB_PASSWORD=XXXXXX
DB_USER=XXXXXX
DB_NAME=XXXXXX
SCHEMA_NAME=XXXXXX
BUCKET_NAME=XXXXXX
```
1. Run `bash create_db.sh` to initialise the database schema.
2. Create a python environment and run `pip install -r requirements.txt`.
3. Run `python3 seed.py` to seed the database with initial metadata about plants, botanists, and locations.
4. Run `bash dockerise.sh` to Dockerise and upload the container to the ECR repo.


## 📄 Files Explained
- `extract_short.py`: Collects plant data by sending API calls.
    - `async_api_call.py` is used to make the calls asynchronous, improving efficiency.
- `transform_short.py`: Transforms the collected data from `json` into a format that is ready to go to the database.
- `load_short.py`: Uploads the output of `transform_short.py` to the RDS.
- `pipeline.py`: Runs all of the above files together.
- `seed.py`: Seeds the database with metadata on the plants.
- `database_handler.py`: Queries the database to gather data whenever required.
- `test_extract_short.py`, `test_transform_short.py`, `test_load_short.py`: Test files for the corresponding scripts.
- `schema.sql`: Sets up the database with initial tables.
- `create_db.sh`: Uses `schema.sql` to set up the cloud RDS.
- `connect.sh`: Connects to the short term database.
- `dockerise.sh`: Dockerises and uploads the image to the ECR.
- `Dockerfile`: Dockerisation instructions.