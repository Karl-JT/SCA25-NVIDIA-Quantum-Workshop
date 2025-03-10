FROM nvcr.io/nvidia/quantum/cuda-quantum:cu12-0.9.1

# Set environment variables to optimize Python in Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Create and set working directory
WORKDIR /workspace

# Copy demo material to workspace
COPY ./algorithm/ /workspace/algorithm/
COPY ./results_H1-1E/ /workspace/results_H1-1E/
COPY ./results_H1-1SC_16_10/ /workspace/results_H1-1SC_16_10/
COPY ./qpe_cudaq.ipynb /workspace/
COPY ./qpe_cudaq_iceberg.ipynb /workspace/
COPY ./qpe_cudaq_iceberg_discard.ipynb /workspace/
COPY ./requirements.txt /workspace/


# Install basic Python packages
RUN pip install --upgrade pip && \
    pip install -r ./requirements.txt
