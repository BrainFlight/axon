FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
# COPY requirements.in .
# RUN pip install --no-cache-dir -r requirements.in
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy source code
COPY protos/ protos/
COPY src/ src/

# Generate gRPC code
RUN python -m grpc_tools.protoc \
    -I protos \
    --python_out=src \
    --grpc_python_out=src \
    protos/inference.proto

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import grpc; grpc.insecure_channel('localhost:50051').channel_ready_future().result(timeout=30)"

EXPOSE 50051

CMD ["python", "src/server.py"]
