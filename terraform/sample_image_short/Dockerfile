FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
COPY main.py .

RUN pip install -r requirements.txt

CMD [ "main.lambda_handler"]