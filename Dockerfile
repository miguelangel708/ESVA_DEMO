FROM python:3.10.11

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    gcc \
    g++

RUN pip install -r requirements.txt

ENTRYPOINT streamlit run ESVA_interface.py
