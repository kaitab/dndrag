FROM python:3.12-alpine
WORKDIR /dndrag

COPY . .

#  COPY requirements.txt ./
RUN pip install .



CMD ["python", "run.py"]