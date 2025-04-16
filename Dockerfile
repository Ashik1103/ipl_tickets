# Use an official Python base image
FROM python:3.11-slim

# Prevent prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator3-1 \
    fonts-liberation \
    xdg-utils \
    libu2f-udev \
    chromium \
    chromium-driver \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Chrome binary path
ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

# Set workdir
WORKDIR /app

# Copy app files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 10000

# Start the Flask app
CMD ["python", "app.py"]
