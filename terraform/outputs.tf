# Describe information terraform should share with you.

output "task_definition_id" {
    value = aws_ecs_task_definition.pharmazer-etl-pipeline-td.arn
}
