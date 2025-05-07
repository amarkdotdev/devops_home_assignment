FROM python:3.11-alpine

WORKDIR /app

# Install system packages needed for OpenSSL
RUN apk add --no-cache build-base openssl

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code, including certs
COPY . .

# Expose HTTPS port
EXPOSE 8443

# Run via HTTPS
ENTRYPOINT ["python", "run_https.py"]
