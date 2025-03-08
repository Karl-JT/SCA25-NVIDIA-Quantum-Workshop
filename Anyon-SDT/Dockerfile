FROM nvcr.io/nvidia/cuda:12.8.0-devel-ubuntu22.04

# Set environment variables to optimize Python in Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install git and build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python-is-python3 \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /workspace

# Copy workshop materials to workspace
COPY ./src_cudaq/ /workspace/src_cudaq/
COPY ./QAOA_CudaQ.ipynb /workspace/
COPY ./src_pennylane/ /workspace/src_pennylane/
COPY ./QAOA_PennyLane.ipynb /workspace/
COPY ./requirements.txt /workspace/
COPY ./anyon-sdt.sh /workspace/
COPY ./README.md /workspace/

# Install Python packages
RUN pip install --upgrade pip && \
    pip install jupyterlab cudaq
RUN pip install -r ./requirements.txt
