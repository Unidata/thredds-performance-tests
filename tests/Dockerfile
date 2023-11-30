FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    # ApacheBench
    apt-get update && \
    apt-get install -y apache2-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY configs configs
COPY run.py run.py
COPY version version

ENTRYPOINT [ "python", "./run.py" ]
