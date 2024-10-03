# Specifies latest image of python
FROM python:latest

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY extract_dashboard.py .
COPY transform_dashboard.py .
COPY longterm_extract.py .
COPY longterm_transform.py .
COPY load_dashboard.py .

# Runs pipeline
CMD ["streamlit", "run", "load_dashboard.py"]