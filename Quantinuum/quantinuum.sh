#!/bin/bash

if [ -z "$1" ]; then 
	echo "Usage: $0 <port_number>"
	exit 1
fi

PORT=$1

docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --user="cudaq" -p $PORT:$PORT -v ${PWD}:/workspace/ nvcr.io/nvidia/quantum/cuda-quantum:cu12-0.9.1 -c "cd /workspace/ && jupyter-lab --port=$PORT --ip=0.0.0.0 --allow-root"

