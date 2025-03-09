#!/bin/bash 

CXX=nvc++
MPICXX=mpic++
if [ ! -z $1 ]; then
    CXX=$1
fi
if [ ! -z $2 ]; then
    MPICXX=$2
fi

devicetype=cuda
OMPFLAGS=-mp
# first is serial
buildtypes=("CUDA Serial" "CUDA OpenMP" "CUDA MPI" "CUDA MPI+OpenMP")
buildnames=("_cuda" "_cuda_omp" "_cuda_mpi" "_cuda_mpi_omp")
compilers=(${CXX} ${CXX} "${MPICXX}" "${MPICXX}")
extraflags=("-D_CUDA" "-D_CUDA ${OMPFLAGS}" "-D_CUDA -D_MPI ${MPIFLAGS}" "-D_CUDA -D_MPI ${MPIFLAGS} ${OMPFLAGS}")
CXXFLAGS="-Xcompiler -fPIC -Xcompiler -std=c++17 -O3 -cuda"


for ((i=0;i<4;i++)) 
do 
    echo "BUILDNAME=${buildnames[$i]} BUILDNAME=${buildnames[$i]} DEVICETYPE=${devicetype}"
    make BUILDNAME=${buildnames[$i]} BUILDNAME=${buildnames[$i]} DEVICETYPE=${devicetype} clean
    make CXXFLAGS="${CXXFLAGS}" BUILDNAME=${buildnames[$i]} BUILDNAME=${buildnames[$i]} DEVICETYPE=${devicetype} CXX="${compilers[$i]}" COMPILER="${compilers[$i]}" EXTRAFLAGS="${extraflags[$i]}" -j
done

