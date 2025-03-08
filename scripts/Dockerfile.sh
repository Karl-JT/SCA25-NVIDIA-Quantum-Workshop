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
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/figure/ /workspace/figure/
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/grovers/ /workspace/grovers/
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/output/ /workspace/output/
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/profile_util/ /workspace/profile_util
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/cudaq-qibolab-emulator-demo.ipynb /workspace/
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/CUDAQ_example.ipynb /workspace/
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/Makefile /workspace/
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/Benchmarking_example.ipynb /workspace/
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/example_output.tgz /workspace/
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/make_profile_util_lib.sh /workspace/
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/req.txt /workspace/
COPY /srv/SCA25-NVIDIA-Quantum-Workshop/Pawsey/workshop_utils.py /workspace/

# Install basic Python packages
RUN pip install --upgrade pip && \
    pip install -r /workspace/req.txt
