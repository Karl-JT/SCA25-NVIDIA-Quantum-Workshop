#!/bin/bash

if [ -z "$1" ]; then 
	echo "Usage: $0 <port_number>"
	exit 1
fi

PORT=$1

docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -p $PORT:$PORT anyon-ihpc:latest jupyter-lab --port=$PORT --ip=0.0.0.0 --allow-root

