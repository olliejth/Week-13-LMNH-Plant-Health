# Specifies latest image of python
FROM python:latest

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY extract_long.py .
COPY transform_long.py .
COPY load_long.py .
COPY pipeline_long.py .

# Runs pipeline
CMD ["python", "pipeline_long.py"]
