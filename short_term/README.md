# Short Term ETL
This folder contains scripts that upload recordings from the plants to the S3 bucket, and will be executed every minute.

## Setup
Please ensure that there is a `.env` file with the following values:
```bash
DB_HOST=XXXXXX
DB_PASSWORD=XXXXXX
DB_USER=XXXXXX
DB_NAME=XXXXXX
SCHEMA_NAME=XXXXXX
BUCKET_NAME=XXXXXX
```
## Files explained
