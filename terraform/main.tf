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
            AWS_rvbyaulf_KEY = var.AWS_ACCESS_KEY
            AWS_rvbyaulf_SECRET_KEY = var.AWS_SECRET_ACCESS_KEY
            DB_HOST     = var.DB_HOST
            DB_PORT     = var.DB_PORT
            DB_NAME     = var.DB_NAME
            DB_USER     = var.DB_USER
            DB_PASSWORD = var.DB_PASSWORD
        }
    }

    image_config { command = ["pipeline.lambda_handler"] }
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

resource "aws_cloudwatch_log_group" "lmnh_etl_long_term_etl__log_group" {
    name = "/ecs/c13-rvbyaulf-lmnh-long-term-etl-pipeline"
}

resource "aws_security_group" "lmnh_etl_long_term_etl_sg" {
    name   = "c13-rvbyaulf-lmnh-long-term-etl-sg"
    vpc_id = data.aws_vpc.c13-vpc.id

    ingress = [
        {
            from_port        = 0
            to_port          = 0
            protocol         = "-1"
            cidr_blocks      = ["0.0.0.0/0"]
            description      = "Allow all inbound traffic"
            ipv6_cidr_blocks = []
            prefix_list_ids  = []
            security_groups  = []
            self             = false
        }
    ]

    egress = [
        {
            from_port        = 0
            to_port          = 0
            protocol         = "-1"
            cidr_blocks      = ["0.0.0.0/0"]
            description      = "Allow all outbound"
            ipv6_cidr_blocks = []
            prefix_list_ids  = []
            security_groups  = []
            self             = false
        }
    ]
}

resource "aws_ecs_task_definition" "lmnh_etl_long_term_etl_td" {
    family                   = "c13-rvbyaulf-lmnh-long-term-etl-task-definition"
    requires_compatibilities = ["FARGATE"]
    network_mode             = "awsvpc"
    cpu                      = "256"
    memory                   = "1024"
    execution_role_arn       = data.aws_iam_role.execution_role.arn

    container_definitions = jsonencode([
        {
            name      = "lmnh-long-term-etl-pipeline"
            image     = data.aws_ecr_image.lmnh_plants_etl_long_term.image_uri
            essential = true
            memory    = 1024
            environment = [
                {
                    name  = "AWS_rvbyaulf_KEY"
                    value = var.AWS_ACCESS_KEY
                },
                {
                    name  = "AWS_rvbyaulf_SECRET_KEY"
                    value = var.AWS_SECRET_ACCESS_KEY
                },
                {
                    name  = "BUCKET_NAME"
                    value = var.BUCKET_NAME
                },
                {
                    name  = "REGION"
                    value = var.REGION
                },
                {
                    name  = "DB_HOST"
                    value = var.DB_HOST
                },
                {
                    name  = "DB_PORT"
                    value = var.DB_PORT
                },
                {
                    name  = "DB_USER"
                    value = var.DB_USER
                },
                {
                    name  = "DB_PASSWORD"
                    value = var.DB_PASSWORD
                },
                {
                    name  = "DB_NAME"
                    value = var.DB_NAME
                },
                {
                    name  = "SCHEMA_NAME"
                    value = var.SCHEMA_NAME
                },
            ]
            logConfiguration = {
                logDriver = "awslogs"
                options = {
                    awslogs-group         = "/ecs/c13-rvbyaulf-lmnh-long-term-etl-pipeline"
                    awslogs-region        = var.REGION
                    awslogs-stream-prefix = "ecs"
                }
            }
        }
    ])
}

data "aws_iam_policy_document" "eventbridge_long_term_schedule_trust_policy" {
    statement {
        effect = "Allow"
        principals {
            type        = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }
        actions = ["sts:AssumeRole"]
    }
}

resource "aws_iam_role" "eventbridge_long_term_scheduler_role" {
    name               = "c13-rvbyaulf-lmnh-etl-long-term-eventbridge-scheduler-role"
    assume_role_policy = data.aws_iam_policy_document.eventbridge_long_term_schedule_trust_policy.json
}

resource "aws_iam_role_policy" "eventbridge_ecs_invocation_policy" {
    name = "EventBridgeECSInvocationPolicy"
    role = aws_iam_role.eventbridge_long_term_scheduler_role.id

    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Effect = "Allow",
                Action = "ecs:RunTask",
                Resource = aws_ecs_task_definition.lmnh_etl_long_term_etl_td.arn
            },
            {
                Effect = "Allow",
                Action = "iam:PassRole",
                Resource = data.aws_iam_role.execution_role.arn
            }
        ]
    })
}

resource "aws_scheduler_schedule" "long_term_etl_schedule" {
    name        = "c13-rvbyaulf-lmnh-etl-long-term-schedule"
    description = "Scheduled rule to trigger the long-term ETL ECS task every 24 hours"
    schedule_expression = "cron(0 0 * * ? *)"  # Runs every day at midnight UTC

    flexible_time_window {
        mode = "OFF"
    }

    target {
        arn       = data.aws_ecs_cluster.c13_cluster.arn
        role_arn  = aws_iam_role.eventbridge_long_term_scheduler_role.arn
        ecs_parameters {
            task_definition_arn = aws_ecs_task_definition.lmnh_etl_long_term_etl_td.arn
            launch_type = "FARGATE"

            network_configuration {
                assign_public_ip = true
                security_groups = [aws_security_group.lmnh_etl_long_term_etl_sg.id]
                subnets = [var.SUBNET_ID, var.SUBNET_ID2, var.SUBNET_ID3]
            }
        }
    }
}

resource "tls_private_key" "private_key" {
    algorithm = "RSA"
    rsa_bits = 4096
}

resource "aws_key_pair" "key_pair" {
    key_name = "c13-rvbyaulf-lmnh-key-pair"
    public_key = tls_private_key.private_key.public_key_openssh
}

resource "aws_security_group" "ec2-sg" {
    name = "c13-rvbyaulf-ec2-security-group"
    vpc_id = data.aws_vpc.c13-vpc.id
    ingress = [
        {
            from_port = 22
            to_port = 22
            protocol = "TCP"
            cidr_blocks = ["0.0.0.0/0"]
            description = "Allow ssh"
            ipv6_cidr_blocks = []
            prefix_list_ids = []
            security_groups = []
            self = false
        }
    ]
    egress = [
        {   
            from_port = 0
            to_port = 0
            protocol = "-1"
            cidr_blocks = ["0.0.0.0/0"]
            description = "Allow all outbound"
            ipv6_cidr_blocks = []
            prefix_list_ids = []
            security_groups = []
            self = false
        }
    ]
}

resource "aws_instance" "pipeline_ec2" {
    instance_type = "t3.nano"
    tags = {Name: "c13-rvbyaulf-lmnh-plant-dashboard"}
    security_groups = [aws_security_group.ec2-sg.id]
    subnet_id = data.aws_subnet.c13-public-subnet.id
    associate_public_ip_address = true
    ami = "ami-0c0493bbac867d427"
    key_name = aws_key_pair.key_pair.key_name
    user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y python3
              sudo yum install -y git
              EOF
}