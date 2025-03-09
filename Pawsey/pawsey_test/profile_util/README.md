# profile_util
Simple C++ library to report memory, timing, thread affinity, parallelism, gpu information. 

The library can be build for serial only codes, OpenMP, MPI, CUDA/HIP and the combination therein. It only makes use of C++17 standard libraries for serial and OpenMP builds and requires MPI and CUDA/HIP for builds that report MPI and GPU related information. 

## Using the library
The library has a simple set of C++ APIs that can be found in `include/profile_util_api.h`. These calles are defined using macros.

### API
The API can be split into several categories. 
#### General information

- `LogParallelAPI()`: reports the parallel API's used. Example output is 
```
[00000] @main L962 (Tue Oct 10 16:14:40 2023) :
Parallel API's
========
MPI Comm world size 2
OpenMP version 201811 with total number of threads = 8 with total number of allowed levels 1
Using GPUs: Running with HIP and found 4 devices
```
That is it reports the rank (here rank 0), the function the routine has been called from, the line in the file, the time and the rest. All calls will follow this format. 
- `MPIRank0ParallelAPI()`: like `LogParallelAPI` but just rank 0 reports this global information. 

#### Core and GPU affinity

- `LogBinding()`: reports the overall binding of cores, GPUs. Example output is 
```
Core Binding
========
On node nid003012 : MPI Rank 0 :  OMP Thread 0 :  at nested level 1 :  Core affinity = 0-7
On node nid003012 : MPI Rank 0 :  OMP Thread 4 :  at nested level 1 :  Core affinity = 0-7
On node nid003012 : MPI Rank 0 :  OMP Thread 1 :  at nested level 1 :  Core affinity = 0-7
On node nid003012 : MPI Rank 0 :  OMP Thread 7 :  at nested level 1 :  Core affinity = 0-7
On node nid003012 : MPI Rank 0 :  OMP Thread 3 :  at nested level 1 :  Core affinity = 0-7
On node nid003012 : MPI Rank 0 :  OMP Thread 2 :  at nested level 1 :  Core affinity = 0-7
On node nid003012 : MPI Rank 0 :  OMP Thread 5 :  at nested level 1 :  Core affinity = 0-7
On node nid003012 : MPI Rank 0 :  OMP Thread 6 :  at nested level 1 :  Core affinity = 0-7
Current runtime environment gpu list is :0,1,2,3        On node nid003012 : MPI Rank 0 : GPU device 0 Device_Name= Bus_ID=0000:c1:00.0 Compute_Units=110 Max_Work_Group_Size=64 Local_Mem_Size=65536 Global_Mem_Size=68702699520
On node nid003012 : MPI Rank 0 : GPU device 1 Device_Name= Bus_ID=0000:c6:00.0 Compute_Units=110 Max_Work_Group_Size=64 Local_Mem_Size=65536 Global_Mem_Size=68702699520
On node nid003012 : MPI Rank 0 : GPU device 2 Device_Name= Bus_ID=0000:c9:00.0 Compute_Units=110 Max_Work_Group_Size=64 Local_Mem_Size=65536 Global_Mem_Size=68702699520
On node nid003012 : MPI Rank 0 : GPU device 3 Device_Name= Bus_ID=0000:ce:00.0 Compute_Units=110 Max_Work_Group_Size=64 Local_Mem_Size=65536 Global_Mem_Size=68702699520
On node nid003012 : MPI Rank 1 :  OMP Thread 0 :  at nested level 1 :  Core affinity = 8-15
On node nid003012 : MPI Rank 1 :  OMP Thread 4 :  at nested level 1 :  Core affinity = 8-15
On node nid003012 : MPI Rank 1 :  OMP Thread 3 :  at nested level 1 :  Core affinity = 8-15
On node nid003012 : MPI Rank 1 :  OMP Thread 5 :  at nested level 1 :  Core affinity = 8-15
On node nid003012 : MPI Rank 1 :  OMP Thread 7 :  at nested level 1 :  Core affinity = 8-15
On node nid003012 : MPI Rank 1 :  OMP Thread 1 :  at nested level 1 :  Core affinity = 8-15
On node nid003012 : MPI Rank 1 :  OMP Thread 6 :  at nested level 1 :  Core affinity = 8-15
On node nid003012 : MPI Rank 1 :  OMP Thread 2 :  at nested level 1 :  Core affinity = 8-15
Current runtime environment gpu list is :0,1,2,3        On node nid003012 : MPI Rank 1 : GPU device 0 Device_Name= Bus_ID=0000:d1:00.0 Compute_Units=110 Max_Work_Group_Size=64 Local_Mem_Size=65536 Global_Mem_Size=68702699520
On node nid003012 : MPI Rank 1 : GPU device 1 Device_Name= Bus_ID=0000:d6:00.0 Compute_Units=110 Max_Work_Group_Size=64 Local_Mem_Size=65536 Global_Mem_Size=68702699520
On node nid003012 : MPI Rank 1 : GPU device 2 Device_Name= Bus_ID=0000:d9:00.0 Compute_Units=110 Max_Work_Group_Size=64 Local_Mem_Size=65536 Global_Mem_Size=68702699520
On node nid003012 : MPI Rank 1 : GPU device 3 Device_Name= Bus_ID=0000:de:00.0 Compute_Units=110 Max_Work_Group_Size=64 Local_Mem_Size=65536 Global_Mem_Size=68702699520
```
Here you can see that for every mpi process, the code reports all the threads and there core affinity, and the GPUs and all their information.
- `MPIRank0LogBinding()`: like `LogBinding()` but just rank 0 reports this global information. 
- `LogThreadAffinity()`: reports core affinity of mpi ranks (if MPI enabled) and openmp threads (if enabled) to standard out. Also reports function and line at which report was requested. For MPI, MPI_COMM_WORLD is used
- `LoggerThreadAffinity(ostream)`: like `LogThreadAffinity` but output to ostream. There are `Logger` interfaces for all calls so that the code can provide a specific ostream. 
- `MPILogThreadAffinity(comm)`: if MPI enabled, can also provide a specific communicator. Like `LogThreadAffinity`. 
- `MPILoggerThreadAffinity(ostream,comm)`: like `LoggerThreadAffinity(ostream)` but for specific communicator, like `MPILogThreadAffinity(comm)`.

#### Memory usage
Calls that report the memory usage and state.
- `LogMemUsage()`: like `LogThreadAffinity` but reports current and peak memory usage by the process to standard out.
- `LoggerMemUsage(ostream)`: like `LogMemUsage` but to ostream. 
- `MPILog0NodeMemUsage()`: like `LogMemUsage()` but generates report for all MPI processes. Example output is:
```
[00000] @main L947 (Wed Jul 24 11:00:56 2024) : Node memory report @ main L947 :
    Node : nid002950^@ : VM current/peak/change : 33.097 [GiB] / 91.230 [MiB] / 0 [B]; RSS current/peak/change : 183.777 [MiB] / 0 [B] / 0 [B]
    Node : nid002984^@ : VM current/peak/change : 33.097 [GiB] / 91.148 [MiB] / 0 [B]; RSS current/peak/change : 182.355 [MiB] / 0 [B] / 0 [B]
```
- `LogSystemMem()`: reports the memory state of the node on which the process is running.
- `LoggerSystemMem(ostream)`: like `LogSystemMem` but to ostream.
- `MPILog0NodeSystemMem()`: like `LogSystemMem` but generates report for all nodes in `MPI_COMM_WORLD`. Example output is
```
[00000] @main L948 (Wed Jul 24 11:00:56 2024) : Node system memory report @ main L948 :
    Node : nid002950^@ : Total : 251.193 [GiB]; Used  : 24.997 [GiB]; Free  : 229.620 [GiB]; Shared: 1.429 [GiB]; Cache : 7.451 [GiB]; Avail : 226.196 [GiB];
    Node : nid002984^@ : Total : 251.193 [GiB]; Used  : 24.155 [GiB]; Free  : 232.222 [GiB]; Shared: 2.038 [GiB]; Cache : 4.538 [GiB]; Avail : 227.038 [GiB];
```

#### Timer usage
This allows code to be profiled with simple additions to the code. Does require creating a timer with `auto timer = NewTimer();`.
- `LogTimeTaken(timer)`: reports the time taken from creation of Timer to point at which logger called and also reports function and line at creation of timer and when request for time taken. Example output:
```
@allocate_mem_host L132 (Wed Jul 24 13:41:03 2024) : Time taken between : @allocate_mem_host L132 - @allocate_mem_host L106 : 1.296 [s]
```
- `LoggerTimeTaken(ostream,timer)`: like `LogTimeTaken(timer)` but to ostream. 
- `LogTimeTakenOnDevice(timer)`: reports the time taken on the gpu device from the creation of the Timer and when it is called. This makes use of the creation of device events. If the current device is not the one upon creation, the code will move to the device upon creation to get the elapsed time and then move back to the current device. Example output:
```
@allocate_mem_gpu L177 (Wed Jul 24 13:41:03 2024) : Time taken on device between : @allocate_mem_gpu L177 - @allocate_mem_gpu L158 : 33 [us]
``` 
- `LoggerTimeTakenOnDevice(ostream,timer)`: like `LogTimeTakenOnDevice(timer)` but to ostream. 

#### Sampler usage
This allows code to be profiled with simple additions to the code using external processes to get quantities like CPU usage, GPU usage and energy. Does require creating a sampler with `auto sampler = NewSampler(sample_time_in_seconds);`. The sampler makes use of concurrent threads running processes like `ps -o %cpu | tail -n 1"` at an specific interval, storing the data in a hidden file `.sampler.cpu_usage.<unique_id>.txt` which is then processed to report back statistics of this data over some interval.
- `LogCPUUsage(sampler)`: reports the cpu usage and time sampled from creation of sampler to point at which logger called and also reports function and line at creation of timer and when request for time taken. Example output:
```
@main L386 (Wed Jul 24 13:41:19 2024) : CPU Usage (%) statistics taken between : @main L386 - @main L353 over 15.532 [s] :  [ave,std,min,max] = [ 4458.294, 78.093, 95.200, 5536.000 ]
```
- `LoggerCPUUsage(ostream,sampler)`: like `LogCPUUsage(sampler)` but to ostream. 
- `LogGPUUsage(sampler)`: reports the gpu usage of all visible gpus to the process and time sampled from creation of sampler to point at which logger called and also reports function and line at creation of timer and when request for time taken. Relies on using `nvidia-smi` or `rocm-smi`. Example output: 
```
@main L387 (Wed Jul 24 13:41:19 2024) : GPU0 Usage (%) statistics taken between : @main L387 - @main L353 over 15.559 [s] :  [ave,std,min,max] = [ 75.558, 3.619, 0.000, 100.000 ]
```
- `LogGPUEnergy(sampler)`: like `LogGPUUsage(sampler)` but reports power consumption along with total energy consumed. Example output: 
```
@main L387 (Wed Jul 24 13:41:19 2024) : GPU0 Power (%) statistics taken between : @main L387 - @main L353 over 15.559 [s] :  [ave,std,min,max] = [ 425.953, 13.413, 118.820, 596.780 ]  GPU Energy (Wh) used = 15.9732
```
- `LogGPUMem(sampler)`: like `LogGPUUsage(sampler)` but reports memory. 
- `LogGPUMemUsage(sampler)`: like `LogGPUUsage(sampler)` but reports memory in percent used. 
- `Logger*(ostream,sampler)`: interfaces which use a specified ostream.
- `LogGPUStatistics(sampler)`: like `LogGPUUsage(sampler)` but reports all aspects of GPU state (usage, memory usage, power). 
 
### Fortran and C API

The Main API is through extern C functions. This is still a work in progress

For C, the name convention follows the C++ expect there is a `_` between words and all are lower case. For examle `LogParallelAPI` -> `log_parallel_api()`.

### Linking the library
It is simply a matter of linking the library with `-L/<path_to_lib> -lprofile_util -std=c++17`

## Build
The library can be built two different ways, one using `cmake` and the other using some `bash` scripts. 

### Cmake
The CMake build relies on users following common steps used by other packages:
```bash
mkdir -p build
cd build
cmake ../ <cmake_args>
```
The default setup will try to build a OpenMP + MPI version of the code if the appropriate libraries are present. Different builds rely on the following options
```cmake
pu_option(ENABLE_MPI "Enable mpi" ON)
pu_option(ENABLE_OPENMP "Enable OpenMP" ON)
pu_option(ENABLE_CUDA "Enable CUDA" OFF)
pu_option(ENABLE_HIP "Enable HIP" OFF)
pu_option(ENABLE_HIP_AMD "Enable HIP with AMD (ROCM)" ON)
pu_option(PU_ENABLE_SHARED_LIB "Enable shared library" ON)
```

Note that the HIP support does assume at a low level that `rocm-smi` exists for some of the profiling information but can be compiled to support HIP calling CUDA so long as the `_HIP_PLATFORM_AMD_` is appropriately *NOT* defined. However, we recommend just building the CUDA version in such circumstances

### Bash/Make
The library comes with some bash scripts `build_cpu.sh`, `build_cuda.sh`, and `build_hip.sh`. These scripts call a simple Makefile which builds a variety of different versions of the libraries. For instance `build_cpu.sh` will build cpu-only (no gpu) versions of the library:
- serial: `libprofile_util.so`
- OpenMP: `libprofile_util_omp.so`
- MPI: `libprofile_utils_mpi.so`
- MPI+OpenMP: `libprofile_util_mpi_omp.so`

The idea behind these scripts is to quickly build versions of the library that can be used to compile the examples provided. 

## Examples
There are several MPI+OpenMP, OpenMP, GPU+OpenMP and GPU+MPI+OpenMP examples contained in the `examples/` directory. These can highlight how to build codes and make use of the libraries API. 
