FROM nvcr.io/nvidia/cuda:12.8.0-devel-ubuntu22.04

# Set environment variables to optimize Python in Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python-is-python3 \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /workspace

# Copy demo material to workspace
COPY ./figures/ /workspace/figures/
COPY ./grovers/ /workspace/grovers/
COPY ./output/ /workspace/output/
COPY ./profile_util/ /workspace/profile_util/
COPY ./Benchmarking_example.ipynb /workspace/
COPY ./CUDAQ_example.ipynb /workspace/
COPY ./Makefile /workspace/
COPY ./example_output.tgz /workspace/
COPY ./make_profile_util_lib.sh /workspace/
COPY ./req.txt /workspace/
COPY ./workshop_utils.py /workspace/

# Install basic Python packages
RUN pip install --upgrade pip && \
    pip install -r ./req.txt && \
    pip install cudaq
