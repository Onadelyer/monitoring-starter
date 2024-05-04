FROM python:3.9

# Install Node Exporter
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl

RUN wget -O /tmp/node_exporter.tar.gz https://github.com/prometheus/node_exporter/releases/download/v${NODE_EXPORTER_VERSION:-latest}/node_exporter-${NODE_EXPORTER_VERSION:-latest}.linux-amd64.tar.gz

RUN mkdir /node_exporter && tar -zxvf /tmp/node_exporter.tar.gz -C /node_exporter

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY conf/test_app.py /app

# Expose ports
EXPOSE 9100

# Start both Node Exporter and your script
CMD ["node_exporter", "&", "python", "load_generator.py"]
