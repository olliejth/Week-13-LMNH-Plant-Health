# Specifies latest image of python
FROM python:latest

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY extract.py .
COPY transform.py .
COPY load.py .
COPY pipeline.py .

# Runs pipeline
CMD ["python", "pipeline.py"]