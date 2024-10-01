# Describe information terraform should share with you.

output "etl_short_term_lambda_arn" {
    value = aws_lambda_function.lmnh_etl_short_term_lambda.arn
}
