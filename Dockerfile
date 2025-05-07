# ────────────────────────────────────────────────────────────
#  GitLab HTTPS FastAPI microservice  •  python:3.11‑alpine
# ────────────────────────────────────────────────────────────
FROM python:3.11-alpine

# 1. Base setup
WORKDIR /app
RUN apk add --no-cache build-base openssl

# 2. Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. App source
COPY main.py .

# 4. Generate self‑signed TLS cert (dev convenience)
RUN mkdir -p certs && \
    openssl req -x509 -newkey rsa:4096 -nodes \
        -keyout certs/key.pem \
        -out   certs/cert.pem \
        -days 365 \
        -subj "/CN=localhost"

# 5. Expose HTTPS port
EXPOSE 8443

# 6. Launch FastAPI via Uvicorn (HTTPS)
ENTRYPOINT ["python", "main.py"]
