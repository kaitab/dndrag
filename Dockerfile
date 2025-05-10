FROM python:3.13
WORKDIR /dndrag

COPY . .

#  COPY requirements.txt ./
RUN pip install .



CMD ["python", "run.py"]