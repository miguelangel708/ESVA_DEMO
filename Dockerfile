FROM python:3.10.11

# Installation of the necessary dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    gcc \
    g++

# Copy current directory to container in /usr/src/app
COPY . /usr/src/app

# Establish the working directory
WORKDIR /usr/src/app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the input command
CMD ["streamlit", "run", "ESVA_interface.py"]
