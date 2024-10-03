# 🚀 Short Term ETL Pipeline

This folder contains scripts for **extracting data from the short-term RDS**, and then **uploading them to a S3 bucket**. This way, **long-term data** can be stored efficiently, should it ever be needed.

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
AWS_ACCESS_KEY=XXXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXX
BUCKET_NAME=XXXXXXXXXX
EMAIL_RECIPIENT=XXXXXXXXXX
EMAIL_SENDER=XXXXXXXXXX
DB_HOST=XXXXXXX
DB_PORT=XXXX
DB_PASSWORD=XXXXXXXX
DB_USER=XXXXX
DB_NAME=XXXXX
SCHEMA_NAME=XXXXXX
ECR_REGISTRY_ID=XXXXX
ECR_LONG_TERM_REPO_NAME=XXXXX
IMAGE_LONG_TERM_NAME_PIPELINE=XXXXX
```

1. Run the command `bash dockerise.sh`.



## 📄 Files Explained
- `extract_long.py`: Extracts all of the "old" data from the database.
- `transform_long.py`: Prepares the extracted data in the format of a summary.
- `load_long.py`: Uploads the summary data as a `csv` file to the S3 bucket.
- `pipeline_long.py`: Runs all of the above files together.
- `test_extract_long`, `test_transform_long`, `test_load_long`: Test files for the corresponding scripts.
- `connect.sh`: Connects to the short term database.
- `docker`...
- `initialise_db.sh`: Initialises the short term database (delete it?)

