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
EC2_HOST=XXXXX
KEY_PATH=../terraform/c13-rvbyaulf-lmnh-key-pair.pem
```
`EC2_HOST` is the public IPV4 DNS of the EC2 instance.
The `pemkey` gets generated after running the Terraform files.

1. Run `bash upload_dashboard.sh`.
2. Access the dashboard via the EC2 public DNS or private IP followed by :8501 e.g:
ec2-18-171-163-71.eu-west-2.compute.amazonaws.com:8501


## 📄 Files Explained
- `extract_dashboard.py`: Extracts all of the short term data to be visualised.
- `transform_dashboard.py`: Creates the charts using `altair`.
- `load_dashboard.py`: Creates the `streamlit` dashboard and uploads all of the charts to it.
- `connect.sh`: Connects to the short term database.
- `run_dashboard_container`: Once the dashboard is built as a Docker image, this bash script runs it locally.

