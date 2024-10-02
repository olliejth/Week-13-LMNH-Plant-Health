variable "REGION" {
    type = string 
    default = "eu-west-2"
}

variable "VPC_ID" {type = string}
variable "SUBNET_ID" {type = string}
variable "SUBNET_ID2" {type = string}
variable "SUBNET_ID3" {type = string}

variable "AWS_ACCESS_KEY" {type = string}
variable "AWS_SECRET_ACCESS_KEY" {type = string}

variable "BUCKET_NAME" {type = string}

variable "DB_HOST" {type = string}
variable "DB_PORT" {type = string}
variable "DB_PASSWORD" {type = string}
variable "DB_USER" {type = string}
variable "DB_NAME" {type = string}
variable "SCHEMA_NAME" {type = string}