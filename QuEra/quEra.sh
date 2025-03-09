#!/bin/bash

if [ -z "$1" ]; then 
	echo "Usage: $0 <port_number>"
	exit 1
fi

PORT=$1

last_two_digits=${PORT: -2}
device_index=$((10#$last_two_digits % 8))

docker run --gpus '"device='$device_index'"' --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -p $PORT:$PORT --rm quEra:latest jupyter-lab --port=$PORT --ip=0.0.0.0 --allow-root
