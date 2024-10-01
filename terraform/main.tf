provider "aws" {
    region     = var.REGION
    secret_key = var.AWS_SECRET_ACCESS_KEY
    access_key = var.AWS_ACCESS_KEY
}

# =========================== DATA ===========================
data "aws_vpc" "c13-vpc" { id = var.VPC_ID }
data "aws_subnet" "c13-public-subnet" { id = var.SUBNET_ID }
data "aws_subnet" "c13-public-subnet2" { id = var.SUBNET_ID2 }
data "aws_subnet" "c13-public-subnet3" { id = var.SUBNET_ID3 }

data "aws_ecr_image" "lmnh_plants_etl_short_term" {
    repository_name = "c13-rvbyaulf-lmnh-plants-short-term"
    image_tag       = "latest"
}

data "aws_ecr_image" "lmnh_plants_etl_long_term" {
    repository_name = "c13-rvbyaulf-lmnh-plants-long-term"
    image_tag       = "latest"
}

data "aws_s3_bucket" "lmnh_plants_s3_bucket" {bucket = var.BUCKET_NAME}

data "aws_iam_role" "execution_role" { name = "ecsTaskExecutionRole" }
data "aws_ecs_cluster" "c13_cluster" { cluster_name = "c13-ecs-cluster" }
