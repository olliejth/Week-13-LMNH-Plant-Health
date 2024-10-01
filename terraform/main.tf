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

# =========================== Short Term ETL Pipeline ===========================

resource "aws_iam_role" "lambda_execution_role" {
    name               = "c13-rvbyaulf-lmnh-etl-short-term-execution-role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Action    = "sts:AssumeRole",
                Effect    = "Allow",
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "lambda_execution_policy_attachment" {
    role       = aws_iam_role.lambda_execution_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_s3_policy" {
    name = "c13-rvbyaulf-lmnh-etl-short-term-lambda-s3-policy"
    role = aws_iam_role.lambda_execution_role.id

    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Effect = "Allow",
                Action = [
                    "s3:ListBucket"
                ],
                Resource = "arn:aws:s3:::c13-rvbyaulf-lmnh-plants"
            },
            {
                Effect = "Allow",
                Action = [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject"
                ],
                Resource = "arn:aws:s3:::c13-rvbyaulf-lmnh-plants/*"
            },
            {
                Sid = "AllowLambdaFunctionToCreateLogs",
                Action = ["logs:*"],
                Effect = "Allow",
                Resource = ["arn:aws:logs:eu-west-2:129033205317:log-group:/aws/lambda/c13-rvbyaulf-lmnh-etl-short-term-lambda:*"]
            }
        ]
    })
}

resource "aws_lambda_function" "lmnh_etl_short_term_lambda" {
    function_name = "c13-rvbyaulf-lmnh-etl-short-term-lambda"
    image_uri     = data.aws_ecr_image.lmnh_plants_etl_short_term.image_uri
    role          = aws_iam_role.lambda_execution_role.arn

    package_type = "Image"

    timeout = 900
    memory_size = 256

    environment {
        variables = {
            BUCKET_NAME = var.BUCKET_NAME
            DB_HOST     = var.DB_HOST
            DB_PORT     = var.DB_PORT
            DB_NAME     = var.DB_NAME
            DB_USER     = var.DB_USER
            DB_PASSWORD = var.DB_PASSWORD
            DB_SCHEMA   = var.SCHEMA_NAME
        }
    }

    image_config { command = ["main.lambda_handler"] }
}

data "aws_iam_policy_document" "eventbridge_schedule_trust_policy" {
    statement {
        effect = "Allow"
        principals {
            type        = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }
        actions = ["sts:AssumeRole"]
    }
}

resource "aws_iam_role" "eventbridge_scheduler_role" {
    name               = "c13-rvbyaulf-lmnh-etl-short-term-eventbridge-scheduler-role"
    assume_role_policy = data.aws_iam_policy_document.eventbridge_schedule_trust_policy.json
}

resource "aws_iam_role_policy" "eventbridge_lambda_invocation_policy" {
    name = "EventBridgeLambdaInvocationPolicy"
    role = aws_iam_role.eventbridge_scheduler_role.id

    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Effect = "Allow",
                Action = "lambda:InvokeFunction",
                Resource = aws_lambda_function.lmnh_etl_short_term_lambda.arn
            },
            {
                Effect = "Allow",
                Action = "iam:PassRole",
                Resource = aws_iam_role.lambda_execution_role.arn
            }
        ]
    })
}

resource "aws_scheduler_schedule" "short_term_etl_schedule" {
    name        = "c13-rvbyaulf-lmnh-etl-short-term-schedule"
    description = "Scheduled rule to trigger the short-term ETL lambda every minute"
    schedule_expression = "cron(* * * * ? *)"

    flexible_time_window {
        mode = "OFF"
    }

    target {
        arn     = aws_lambda_function.lmnh_etl_short_term_lambda.arn
        role_arn = aws_iam_role.eventbridge_scheduler_role.arn
    }
}

# =========================== Long Term ETL Pipeline ===========================

# resource "aws_ecs_task_definition" "lmnh_etl_long_term_etl_td" {
#     family                   = "c13-rvbyaulf-lmnh-etl-long-term-etl-task-definition"
#     requires_compatibilities = ["FARGATE"]
#     network_mode             = "awsvpc"
#     cpu                      = "256"
#     memory                   = "1024"
#     execution_role_arn       = data.aws_iam_role.execution_role.arn

#     container_definitions = jsonencode([
#         {
#             name      = "pharmazer-etl-pipeline"
#             image     = data.aws_ecr_image.lmnh_plants_etl_long_term.image_uri
#             essential = true
#             memory    = 1024
#             environment = [
#                 {
#                     name  = "AWS_ACCESS_KEY"
#                     value = var.AWS_ACCESS_KEY
#                 },
#                 {
#                     name  = "AWS_SECRET_ACCESS_KEY"
#                     value = var.AWS_SECRET_ACCESS_KEY
#                 },
#                 {
#                     name  = "BUCKET_NAME"
#                     value = var.BUCKET_NAME
#                 },
#                 {
#                     name  = "USER_NAME"
#                     value = var.USER_NAME
#                 },
#                 {
#                     name  = "COHORT_NAME"
#                     value = var.COHORT_NAME
#                 },
#                 {
#                     name  = "REGION"
#                     value = var.REGION
#                 },
#                 {
#                     name  = "DB_HOST"
#                     value = var.DB_HOST
#                 },
#                 {
#                     name  = "DB_PORT"
#                     value = var.DB_PORT
#                 },
#                 {
#                     name  = "DB_USER"
#                     value = var.DB_USER
#                 },
#                 {
#                     name  = "DB_PASSWORD"
#                     value = var.DB_PASSWORD
#                 },
#                 {
#                     name  = "DB_NAME"
#                     value = var.DB_NAME
#                 },
#                 {
#                     name  = "SCHEMA_NAME"
#                     value = var.SCHEMA_NAME
#                 },
#             ]
#             logConfiguration = {
#                 logDriver = "awslogs"
#                 options = {
#                     awslogs-group         = "/ecs/c13-shayak-pharmazer-etl-pipeline"
#                     awslogs-region        = var.REGION
#                     awslogs-stream-prefix = "ecs"
#                 }
#             }
#         }
#     ])
# }