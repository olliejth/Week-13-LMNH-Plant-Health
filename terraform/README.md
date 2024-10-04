# 🚀 Provision Cloud Infrastructure using Terraform
This folder contains the Terraform scripts to provision the necessary cloud infrastructure for the LMNH Plants cloud infrastructure.

## 🛠️ Prerequisites
Before you start, ensure that you have the following configured on your machine:
- **AWS CLI** to interact with AWS services
- **Terraform** installed.
- **Docker** installed for containerisation.

And the following services provisioned:
- **ECR repository** for short term etl.
- **ECR repository** for long term etl.
- **S3 bucket** to store long term plant information. See the `collect_metadata` README.
- **RDS (Microsoft SQL Server)** to store the short term plant information.

## 📂 Setup
Follow these steps to deploy the infrastructure:

1. Clone the repository to your local machine if you haven't already.

2. Perform the short and long term ETL setup by reading `../short_term/README.md` and `../long_term/README.md`

3. Create a `terraform.tfvars` file in this directory with your AWS credentials and infrastructure details:
```bash
AWS_ACCESS_KEY        = "your-aws-access-key"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-key"

REGION                = "your-region"
VPC_ID                = "your-vpc-id"
SUBNET_ID             = "your-subnet-id"
SUBNET_ID2            = "your-second-subnet-id"
SUBNET_ID3            = "your-third-subnet-id"

BUCKET_NAME           = "your-s3-bucket-name"

DB_HOST               = "your-RDS-host"
DB_PORT               = "your-RDS-port"
DB_NAME               = "your-RDS-name"
DB_USER               = "your-RDS-user"
DB_PASSWORD           = "your-RDS-password"
DB_SCHEMA_NAME        = "your-RDS-schema"

ECR_SHORT_TERM_REPO_NAME  =  "name-of-repo-to-store-short-term-etl-image"
ECR_LONG_TERM_REPO_NAME   =  "name-of-repo-to-store-long-term-etl-image"
```

4. Initialize Terraform:
```bash
terraform init
```

5. Review the Terraform plan to ensure everything is set up correctly:
```bash
terraform plan
```

6. Apply the Terraform configuration to provision the infrastructure:
```bash
terraform apply
```

7. Restrict access to the generated pemkey
```bash
chmod 400 c13-rvbyaulf-lmnh-key-pair.pem
```

8. Follow the instructions in `../dashboard/README.md` to setup and run the dashboard.

    This will create the necessary resources for the ETL pipeline, including:
    - Pushing docker images to ECR repos (`../short_term/README.md`, `../long_term/README.md`)
    - Lambda for short-term ETL
    - ECS task definition for the long-term ETL
    - EventBridge schedules to trigger the ETL pipelines
    - IAM roles and policies for Lambda, ECS, and EventBridge
    - EC2 to host the dashboard
    - Running the dashboard (`../dashboard/README.md`)

7. To destroy all provisioned services using terraform:
```bash
terraform destroy
```