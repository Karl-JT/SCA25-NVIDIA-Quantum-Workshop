/*! \file profile_util_gpu.h
 *  \brief this file contains all definitions that are related to GPU macros.
 */


#ifndef _PROFILE_UTIL_GPU
#define _PROFILE_UTIL_GPU

#ifdef _HIP
#define _GPU 
#define _GPU_API "HIP"
#define _GPU_TO_SECONDS 1.0/1000.0
#include <hip/hip_runtime.h>
// #include <hip>
#endif

#ifdef _CUDA
#define _GPU
#define _GPU_API "CUDA"
#define _GPU_TO_SECONDS 1.0/1000.0
#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#endif

#ifdef _OPENMP 
#include <omp.h>
#endif
/// \defgroup GPU related define statements 
//@{
#ifdef _HIP
#define pu_gpuMalloc hipMalloc
#define pu_gpuHostMalloc hipHostMalloc
#define pu_gpuMallocManaged hipMallocManaged
#define pu_gpuFree hipFree
#define pu_gpuHostFree hipHostFree
#define pu_gpuMemcpy hipMemcpy
#define pu_gpuMemcpyHostToDevice hipMemcpyHostToDevice
#define pu_gpuMemcpyDeviceToHost hipMemcpyDeviceToHost
#define pu_gpuEvent_t hipEvent_t
#define pu_gpuEventCreate hipEventCreate
#define pu_gpuEventDestroy hipEventDestroy
#define pu_gpuEventRecord hipEventRecord
#define pu_gpuEventSynchronize hipEventSynchronize
#define pu_gpuEventElapsedTime hipEventElapsedTime
#define pu_gpuDeviceSynchronize hipDeviceSynchronize
#define pu_gpuGetErrorString hipGetErrorString
#define pu_gpuError_t hipError_t
#define pu_gpuErr hipErr
#define pu_gpuSuccess hipSuccess
#define pu_gpuGetDeviceCount hipGetDeviceCount
#define pu_gpuGetDevice hipGetDevice
#define pu_gpuDeviceProp_t hipDeviceProp_t
#define pu_gpuSetDevice hipSetDevice
#define pu_gpuGetDeviceProperties hipGetDeviceProperties
#define pu_gpuDeviceGetPCIBusId hipDeviceGetPCIBusId
#define pu_gpuDeviceReset hipDeviceReset
#define pu_gpuLaunchKernel(...) hipLaunchKernelGGL(__VA_ARGS__)
#define pu_gpuStream_t hipStream_t
#define pu_gpuPeekAtLastError hipPeekAtLastError
#define pu_gpuMemPrefetchAsync hipMemPrefetchAsync

#ifdef __HIP_PLATFORM_AMD__
#define pu_gpuVisibleDevices "ROCR_VISIBLE_DEVICES"
#define pu_gpuMonitorCmd "rocm-smi"
#define pu_gpu_usage_request(ngpus) std::string(" --showuse --csv | head -n ") + std::to_string(1+ngpus) + std::string(" | tail -n ")+std::to_string(ngpus) + std::string(" | sed \"s/,/ /g\" | awk '{print $2}'")
#define pu_gpu_energy_request(ngpus) std::string(" --showpower --csv | head -n ") + std::to_string(1+ngpus) + std::string(" | tail -n ")+std::to_string(ngpus) + std::string(" | sed \"s/,/ /g\" | awk '{print $2}'")
#define pu_gpu_mem_request(ngpus) std::string(" --showmeminfo VRAM --csv | head -n ") + std::to_string(1+ngpus) + std::string(" | tail -n ")+std::to_string(ngpus) + std::string(" | sed \"s/,/ /g\" | awk '{print $3/1000.0/1000.0}'")
#define pu_gpu_memusage_request(ngpus) std::string(" --showmeminfo VRAM --csv | head -n ") + std::to_string(1+ngpus) + std::string(" | tail -n ")+std::to_string(ngpus) + std::string(" | sed \"s/,/ /g\" | awk '{print $3/$2*100.0}'")
#define pu_gpu_formating(ngpus) " "
#else

#define pu_gpuVisibleDevices "CUDA_VISIBLE_DEVICES"
#define pu_gpuMonitorCmd "nvidia-smi"
// commands for querying gpu
#define pu_gpu_energy_request(ngpus) std::string(" --query-gpu=power.draw ")
#define pu_gpu_usage_request(ngpus) std::string(" --query-gpu=utilization.gpu ")
#define pu_gpu_mem_request(ngpus) std::string(" --query-gpu=memory.used ")
#define pu_gpu_memusage_request(ngpus) std::string(" --query-gpu=utilization.memory ")
#define pu_gpu_formating(ngpus) std::string(" --format=csv,noheader,nounits ")
#endif

#endif

#ifdef _CUDA

#define pu_gpuMalloc cudaMalloc
#define pu_gpuHostMalloc cudaMallocHost
#define pu_gpuMallocManaged cudaMallocManaged
#define pu_gpuFree cudaFree
#define pu_gpuHostFree cudaFreeHost
#define pu_gpuMemcpy cudaMemcpy
#define pu_gpuMemcpyHostToDevice cudaMemcpyHostToDevice
#define pu_gpuMemcpyDeviceToHost cudaMemcpyDeviceToHost
#define pu_gpuEvent_t cudaEvent_t
#define pu_gpuEventCreate cudaEventCreate
#define pu_gpuEventDestroy cudaEventDestroy
#define pu_gpuEventRecord cudaEventRecord
#define pu_gpuEventSynchronize cudaEventSynchronize
#define pu_gpuEventElapsedTime cudaEventElapsedTime
#define pu_gpuDeviceSynchronize cudaDeviceSynchronize
#define pu_gpuGetErrorString cudaGetErrorString
#define pu_gpuError_t cudaError_t
#define pu_gpuErr cudaErr
#define pu_gpuSuccess cudaSuccess
#define pu_gpuGetDeviceCount cudaGetDeviceCount
#define pu_gpuGetDevice cudaGetDevice
#define pu_gpuDeviceProp_t cudaDeviceProp
#define pu_gpuSetDevice cudaSetDevice
#define pu_gpuGetDeviceProperties cudaGetDeviceProperties
#define pu_gpuDeviceGetPCIBusId cudaDeviceGetPCIBusId
#define pu_gpuDeviceReset cudaDeviceReset
#define pu_gpuLaunchKernel(kernelfunc, blksize, threadsperblk, shsize, stream, ...) \
kernelfunc<<<blksize,threadsperblk>>>(__VA_ARGS__)
#define pu_gpuStream_t cudaStream_t
#define pu_gpuPeekAtLastError cudaPeekAtLastError
#define pu_gpuMemPrefetchAsync cudaMemPrefetchAsync

#define pu_gpuVisibleDevices "CUDA_VISIBLE_DEVICES"
#define pu_gpuMonitorCmd "nvidia-smi"
// commands for querying gpu
#define pu_gpu_energy_request(ngpus) std::string(" --query-gpu=power.draw ")
#define pu_gpu_usage_request(ngpus) std::string(" --query-gpu=utilization.gpu ")
#define pu_gpu_mem_request(ngpus) std::string(" --query-gpu=memory.used ")
#define pu_gpu_memusage_request(ngpus) std::string(" --query-gpu=utilization.memory ")
#define pu_gpu_formating(ngpus) std::string(" --format=csv,noheader,nounits ")

#endif

#ifdef _GPU 
// macro for checking errors in HIP API calls
#define pu_gpuErrorCheck(call)                                                                 \
do{                                                                                         \
    pu_gpuError_t pu_gpuErr = call;                                                               \
    if(pu_gpuSuccess != pu_gpuErr){                                                               \
        std::cerr<<_GPU_API<<" error : "<<pu_gpuGetErrorString(pu_gpuErr)<<" - "<<__FILE__<<":"<<__LINE__<<std::endl; \
        exit(0);                                                                            \
    }                                                                                       \
}while(0)

#define pu_gpuCheckLastKernel() {pu_gpuErrorCheck(pu_gpuPeekAtLastError()); \
pu_gpuErrorCheck(pu_gpuDeviceSynchronize());}
#endif
//@}

#ifdef _GPU
#ifdef _USE_UNIFIED_GPU_CLASS
//@{
namespace gpu_util
{
///@brief Allocator class for unified memory 
/// This class is based on https://gist.github.com/CommitThis/1666517de32893e5dc4c441269f1029a
template <typename T>
class unified_alloc
{
public:
    using value_type = T;
    using pointer = value_type*;
    using size_type = std::size_t;

    unified_alloc() noexcept = default;

    template <typename U>
    unified_alloc(unified_alloc<U> const&) noexcept {}

    auto allocate(size_type n, const void* = 0) -> value_type* {
        value_type * tmp;
        pu_gpuErrorCheck(pu_gpuMallocManaged((void**)&tmp, n * sizeof(T)));
        return tmp;
    }

    auto deallocate(pointer p, size_type n) -> void {
        if (p) {
            pu_gpuErrorCheck(pu_gpuFree(p));
        }
    }
};

/* Equality operators */
template <class T, class U>
auto operator==(unified_alloc<T> const &, unified_alloc<U> const &) -> bool {
    return true;
}

template <class T, class U>
auto operator!=(unified_alloc<T> const &, unified_alloc<U> const &) -> bool {
    return false;
}

/// Template alias for convenient creating of a vector backed by unified memory 
template <typename T>
using unified_vector = std::vector<T, unified_alloc<T>>;

/*! Define a default type trait; any instantiation of this with a type will
    contain a value of false:
        is_unified<int>::value == false
*/
template<typename T>
struct is_unified : std::false_type{};

/*! A specialisation of the above type trait. If the passed in type is in
    itself a template, and the inner type is our unified allocator, then
    the trait type will contain a true value:
        is_unified<std::vector<int>>::value == false
        is_unified<profile_util::vector<int>>::value == true
    Remembering that the actual signature for both the stdlib and our CUDA 
    vector is something like:
        vector<int, allocator<int>>
*/
template<template<typename, typename> typename Outer, typename Inner>
struct is_unified<Outer<Inner, unified_alloc<Inner>>> : std::true_type{};


/*!  A helper function that retrieves whether or not the passed in type is
    contains a unified allocator inner type, without using the type traits
    directly */
template<typename T>
constexpr static auto is_unified_v = is_unified<T>::value;


/*! This uses template substitution to generate a function that only exists
    for types that contain a unified allocator. If is_unified_v<T> is 
    false, std::enable_if_t does not exist, the substitution will fail, and 
    because it is not an error to have a failed substitution, the function
    will simply not exist.
    
    get_current_device is a utility function that uses the CUDA API to get
    the ID of the current device.
*/
template <typename T, typename = std::enable_if_t<is_unified_v<T>>>
auto prefetch(T const & container,  pu_gpuStream_t stream = 0, 
        int device = 0)
{
    using value_type = typename T::value_type;
    auto p = container.data();
    if (p) {
        pu_gpuErrorCheck(pu_gpuMemPrefetchAsync(p, container.size() *
            sizeof(value_type), device, stream));
    }
}
}
//@}
#endif
#endif

#endif
