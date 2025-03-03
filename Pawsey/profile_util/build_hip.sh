#!/bin/bash 

CXX="hipcc --amdgpu-target=gfx90a -stdlib++-isystem /opt/cray/pe/gcc/12.2.0/snos/include/g++ -stdlib++-isystem /opt/cray/pe/gcc/12.2.0/snos/include/g++/x86_64-suse-linux"
MPICXX="hipcc --amdgpu-target=gfx90a -stdlib++-isystem /opt/cray/pe/gcc/12.2.0/snos/include/g++ -stdlib++-isystem /opt/cray/pe/gcc/12.2.0/snos/include/g++/x86_64-suse-linux"
if [ ! -z $1 ]; then
    CXX=$1
fi
if [ ! -z $2 ]; then
    MPICXX=$2
fi

devicetype=hip
OMPFLAGS="-fopenmp --offload-arch=gfx90a -fopenmp-targets=amdgcn-amd-amdhsa -Xopenmp-target=amdgcn-amd-amdhsa -march=gfx90a"
GPUFLAGS="-D_HIP -D__HIP_PLATFORM_AMD__"
MPIFLAGS="-I${CRAY_MPICH_DIR}/include/"
# first is serial
buildtypes=("HIP Serial" "HIP OpenMP" "HIP MPI" "HIP MPI+OpenMP")
buildnames=("_hip" "_hip_omp" "_hip_mpi" "_hip_mpi_omp")
compilers=("${CXX}" "${CXX}" "${MPICXX}" "${MPICXX}")
extraflags=("${GPUFLAGS}" "${GPUFLAGS} ${OMPFLAGS}" "${GPUFLAGS} -D_MPI ${MPIFLAGS}" "${GPUFLAGS} -D_MPI ${MPIFLAGS} ${OMPFLAGS}")


for ((i=0;i<4;i++)) 
do 
    echo "BUILDNAME=${buildnames[$i]} BUILDNAME=${buildnames[$i]} DEVICETYPE=${devicetype}"
    make BUILDNAME=${buildnames[$i]} BUILDNAME=${buildnames[$i]} DEVICETYPE=${devicetype} clean
    make BUILDNAME=${buildnames[$i]} BUILDNAME=${buildnames[$i]} DEVICETYPE=${devicetype} CXX="${compilers[$i]}" COMPILER="${compilers[$i]}" EXTRAFLAGS="${extraflags[$i]}" -j
done

