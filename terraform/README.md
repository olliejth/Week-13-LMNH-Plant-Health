# Variables to fix

## short term etl lmabda environment variables:

```bash
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
```

## short term etl lmabda handler function name:
```bash
image_config { command = ["main.lambda_handler"] }
```