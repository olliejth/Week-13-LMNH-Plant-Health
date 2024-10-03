# 🚀 Short Term ETL Pipeline

This folder contains scripts to create a **dashboard** that visualises the **short term data**.

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
DB_HOST=XXXXX
DB_PORT=XXXXX
DB_PASSWORD=XXXXX
DB_USER=XXXXX
DB_NAME=XXXXX
SCHEMA_NAME=XXXXX
AWS_ACCESS_KEY=XXXXX
AWS_SECRET_ACCESS_KEY=XXXXX
BUCKET_NAME=XXXXX
DASHBOARD_CONTAINER=XXXXX
```

1. Create a python environment and run `pip install -r requirements.txt`.
2. Build the Docker image, 


## 📄 Files Explained
- `extract_dashboard.py`: Extracts all of the short term data to be visualised.
- `transform_dashboard.py`: Creates the charts using `altair`.
- `load_dashboard.py`: Creates the `streamlit` dashboard and uploads all of the charts to it.
- `connect.sh`: Connects to the short term database.
- `run_dashboard_container`: Once the dashboard is built as a Docker image, this bash script runs it locally.

