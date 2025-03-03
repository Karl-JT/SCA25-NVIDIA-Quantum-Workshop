#!/bin/bash 
cd profile_util
mkdir -p build
cd build 
cmake .. \
 -DCMAKE_CUDA_ARCHITECTURES=90 \
 -DPU_ENABLE_CUDA=ON \
 -DPU_ENABLE_MPI=OFF \
 -DCMAKE_CXX_FLAGS=-cuda 

make -j
OMP_NUM_THREADS=2 ./src/tests/test_profile_util
cd ../../


