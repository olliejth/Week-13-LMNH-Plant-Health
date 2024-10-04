# 🚀 Collect Metadata
This folder contains scripts to pull metadata from the API and upload them to the S3 bucket.

## 🛠️ Prerequisites
Before you start, ensure that you have the following configured on your machine:
- **Python** to run the scripts.


## 📂 Setup
Follow these steps to deploy the infrastructure:

1. Create an environment and run `pip install -r requirements.txt`.
2. Create a `.env` file with the following content:
```bash
AWS_rvbyaulf_KEY=XXXXX
AWS_rvbyaulf_SECRET_KEY=XXXXX
BUCKET_NAME=XXXXX
```
3. Run `python3 pipeline_metadata.py`.

This should create three `csv` files in your S3 bucket, in the `/metadata` directory.