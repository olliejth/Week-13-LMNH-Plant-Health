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
2. Run `python3 seed.py` to seed the database with initial metadata about plants, botanists, and locations.
3. Build the Docker image, and upload to AWS ECR as a lambda.


