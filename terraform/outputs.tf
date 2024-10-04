# Describe information terraform should share with you.

output "etl_short_term_lambda_arn" {
    value = aws_lambda_function.lmnh_etl_short_term_lambda.arn
}

output "EC2_public_ip" {
    value = aws_instance.pipeline_ec2.public_ip
}

output "EC2_public_dns" {
    value = aws_instance.pipeline_ec2.public_dns
}