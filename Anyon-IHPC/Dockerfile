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

# Copy demo material to workspace
COPY ./anyon_2q_CZ/ /workspace/anyon_2q_CZ/
COPY ./anyon_2q_iSWAP/ /workspace/anyon_2q_iSWAP/
COPY ./anyon_4q_CZ/ /workspace/anyon_4q_CZ/
COPY ./demo/ /workspace/demo/
COPY ./cudaq-qibolab-emulator-demo.ipynb /workspace/

# Install basic Python packages
RUN pip install --upgrade pip && \
    pip install jupyterlab matplotlib qutip==4.7.6 qibocal==0.1.1

# Clone qibolab repository, checkout anyon_emulator branch, and install
RUN git clone https://github.com/qiboteam/qibolab.git && \
    cd qibolab && \
    git checkout anyon_emulator && \
    pip install . && \
    cd ..

# Clone qibolab_visualization repository and install
RUN git clone https://github.com/qiboteam/qibolab_visualization.git && \
    cd qibolab_visualization && \
    pip install . && \
    cd ..

# Install additional packages
RUN pip install cudaq scipy==1.12.0
