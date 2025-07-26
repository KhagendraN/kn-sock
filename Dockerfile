FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required by pyaudio and opencv-python
RUN apt-get update && apt-get install -y \
    gcc \
    libportaudio2 \
    portaudio19-dev \
    libasound2 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENTRYPOINT ["python", "-m", "kn_sock.cli"]
