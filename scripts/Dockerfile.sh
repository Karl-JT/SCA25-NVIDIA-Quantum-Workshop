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
COPY ./figure/ /workspace/figure/
COPY ./grovers/ /workspace/grovers/
COPY ./output/ /workspace/output/
COPY ./profile_util/ /workspace/profile_util
COPY ./CUDAQ_example.ipynb /workspace/
COPY ./Makefile /workspace/
COPY ./Benchmarking_example.ipynb /workspace/
COPY ./example_output.tgz /workspace/
COPY ./make_profile_util_lib.sh /workspace/
COPY ./req.txt /workspace/
COPY ./workshop_utils.py /workspace/

# Install basic Python packages
RUN pip install --upgrade pip && \
    pip install -r /workspace/req.txt
