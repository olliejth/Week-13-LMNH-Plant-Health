source .env
docker tag $IMAGE_SHORT_TERM_NAME_PIPELINE:latest $ECR_REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com/$ECR_SHORT_TERM_REPO_NAME:latest
docker tag $IMAGE_LONG_TERM_NAME_PIPELINE:latest $ECR_REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com/$ECR_LONG_TERM_REPO_NAME:latest