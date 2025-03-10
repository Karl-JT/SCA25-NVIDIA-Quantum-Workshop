FROM nvcr.io/nvidia/quantum/cuda-quantum:cu12-0.9.1

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Create and set working directory
WORKDIR /workspace

# Copy demo material to workspace
COPY ./data/ /workspace/data/
COPY ./bloqade_aquila.ipynb /workspace/
COPY ./braket_aquila.ipynb /workspace/
COPY ./cudaq_aquila.ipynb /workspace/
COPY ./kirin_bloqade.ipynb /workspace/


