FROM python:latest

WORKDIR /app

COPY requirements.txt ./
COPY test.py ./

RUN pip install -r requirements.txt
RUN chmod +x test.py

CMD ["python3", "test.py"]