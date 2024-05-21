FROM python:3.9-slim

WORKDIR /app

COPY conf/requirements.txt .
RUN pip install -r requirements.txt

COPY conf/metrics_calculator.py /app

CMD ["python", "metrics_calculator.py"]
