FROM python:3.10

WORKDIR /opt/app

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends build-essential python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -U pip

COPY . .

COPY requirements.txt ./

RUN pip install -U -r requirements.txt

CMD ["python", "./server.py"]