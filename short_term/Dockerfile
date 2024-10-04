# Specifies latest image of python
FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY async_api_call.py .
COPY extract_short.py .
COPY transform_short.py .
COPY load_short.py .
COPY pipeline.py .
COPY database_handler.py .

# Runs pipeline
CMD ["pipeline.lambda_handler"]