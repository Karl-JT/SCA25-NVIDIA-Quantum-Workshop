.PHONY: all clean

CXX=nvq++
MPIFLAGS=-D_MPI -lmpi
FLAGS=-std=c++17 -O2 -Wall -Wextra -Wpedantic -fPIC
PROFILEFLAGS=-I$(shell pwd)/profile_util/include -I/opt/nvidia/cudaq/include -I/opt/nvidia/cudaq/include/cudaq -I/opt/nvidia/cudaq/include/cudaq/algorithms -Wl,-rpath,$(shell pwd)/profile_util/lib -L$(shell pwd)/profile_util/lib -L/opt/nvidia/cudaq/lib
CUDAFLAGS=-D_CUDA -L/opt/nvidia/hpc_sdk/Linux_x86_64/2025/cuda/lib64/ -I/opt/nvidia/hpc_sdk/Linux_x86_64/2025/cuda/include/
LIBS=-lcudart -lprofile_util_cuda -lcudaq

all: grovers_cudaq # grovers_cudaq

clean: 
	rm -f grovers/bin/grovers_cudaq*

grovers_cudaq: profile_util/build/src/libprofile_util.so \
	grovers/bin/grovers_cudaq_cpu_state_vec \
	grovers/bin/grovers_cudaq_cpu_state_vec_fp64 \
	grovers/bin/grovers_cudaq_gpu_state_vec \
	grovers/bin/grovers_cudaq_gpu_state_vec_fp64 \
	grovers/bin/grovers_cudaq_gpu_mps \
	grovers/bin/grovers_cudaq_gpu_mps_fp64 

profile_util/build/src/libprofile_util.so:
	$(shell ./make_profile_util_lib.sh)

grovers/bin/grovers_cudaq_cpu_state_vec: grovers/src/grovers_cudaq.cpp grovers/src/grovers_cudaq.h 
	$(CXX) $(CUDAFLAGS) $(FLAGS) $(PROFILEFLAGS) --target qpp-cpu --target-option fp32 grovers/src/grovers_cudaq.cpp -o grovers/bin/grovers_cudaq_cpu_state_vec $(LIBS)
	rm -f grovers_cudaq.o
  
grovers/bin/grovers_cudaq_cpu_state_vec_fp64: grovers/src/grovers_cudaq.cpp grovers/src/grovers_cudaq.h 
	$(CXX) $(CUDAFLAGS) $(FLAGS) $(PROFILEFLAGS) --target qpp-cpu --target-option fp64 grovers/src/grovers_cudaq.cpp -o grovers/bin/grovers_cudaq_cpu_state_vec_fp64 $(LIBS) 
	rm -f grovers_cudaq.o

grovers/bin/grovers_cudaq_gpu_state_vec: grovers/src/grovers_cudaq.cpp grovers/src/grovers_cudaq.h 
	$(CXX) $(CUDAFLAGS) $(FLAGS) $(PROFILEFLAGS) --target nvidia --target-option fp32 grovers/src/grovers_cudaq.cpp -o grovers/bin/grovers_cudaq_gpu_state_vec $(LIBS) 
	rm -f grovers_cudaq.o
  
grovers/bin/grovers_cudaq_gpu_state_vec_fp64: grovers/src/grovers_cudaq.cpp grovers/src/grovers_cudaq.h 
	$(CXX) $(CUDAFLAGS) $(FLAGS) $(PROFILEFLAGS) --target nvidia --target-option fp64 grovers/src/grovers_cudaq.cpp -o grovers/bin/grovers_cudaq_gpu_state_vec_fp64 $(LIBS) 
	rm -f grovers_cudaq.o

grovers/bin/grovers_cudaq_gpu_mps: grovers/src/grovers_cudaq.cpp grovers/src/grovers_cudaq.h 
	$(CXX) $(CUDAFLAGS) $(FLAGS) $(PROFILEFLAGS) --target tensornet-mps --target-option fp32 grovers/src/grovers_cudaq.cpp -o grovers/bin/grovers_cudaq_gpu_mps $(LIBS) 
	rm -f grovers_cudaq.o

grovers/bin/grovers_cudaq_gpu_mps_fp64: grovers/src/grovers_cudaq.cpp grovers/src/grovers_cudaq.h 
	$(CXX) $(CUDAFLAGS) $(FLAGS) $(PROFILEFLAGS) --target tensornet-mps --target-option fp64 grovers/src/grovers_cudaq.cpp -o grovers/bin/grovers_cudaq_gpu_mps_fp64 $(LIBS) 
	rm -f grovers_cudaq.o

# grovers/bin/grovers_cudaq_sol: grovers/solution/grovers_cudaq.cpp grovers/solution/grovers_cudaq.h 
# 	$(CXX) $(CUDAFLAGS) $(FLAGS) $(PROFILEFLAGS) grovers/solution/grovers_cudaq.cpp -o grovers/bin/grovers_cudaq_sol $(LIBS) 
