FROM python:3.9-slim

WORKDIR /app

COPY conf/requirements.txt .
RUN pip install -r requirements.txt

COPY conf/custom_metrics_app.py /app

CMD ["python", "custom_metrics_app.py"]
