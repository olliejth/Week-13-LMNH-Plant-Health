source .env 
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin $ECR_REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com