#include <array>
#include <iostream>
#include <numeric>
#include <vector>
#include <random>
#include <profile_util.h>

int main(int argc, char *argv[])
{
    int ThisTask = 0;
#ifdef _MPI
    auto comm = MPI_COMM_WORLD;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(comm, &ThisTask);
    MPISetLoggingComm(comm);
#endif 
#ifdef _MPI
    MPILog0Version();
    MPILog0ParallelAPI();
    MPILog0Binding();
    MPILog0NodeSystemMem();
    MPI_Barrier(comm);
#else 
    LogVersion();
    LogParallelAPI();
    LogBinding();
    LogSystemMem();
#endif
    LogMemUsage();
    auto t1 = NewTimerHostOnly();
    auto s1 = NewComputeSampler(0.01);
    //auto st1 = NewSTraceSampler(0.1);
    s1.SetKeepFiles(true);
    sleep(1);
    std::vector<float> xvec(1000000);
    std::default_random_engine generator;
    std::normal_distribution<double> distribution(1.0,2.0);
    for (auto &x:xvec) 
    {
        x = distribution(generator);
        x = exp(-x*x)*x/(1.0+x)+sin(pow(x*x,0.25));
    }
    LogCPUUsage(s1);
    LogTimeTaken(t1);

#ifdef _GPU
    auto Nentries = xvec.size();
    int nDevices;
    std::vector<float*> xdev;
    pu_gpuErrorCheck(pu_gpuGetDeviceCount(&nDevices));
    xdev.resize(nDevices);
    auto tgpumem = NewTimerHostOnly();
    for (auto idev=0;idev<nDevices;idev++) {
        pu_gpuErrorCheck(pu_gpuSetDevice(idev));
        auto time_local = NewTimer();
        auto sgpu = NewComputeSampler(0.01);
        auto nbytes = Nentries * sizeof(float);
        pu_gpuErrorCheck(pu_gpuMalloc(&xdev[idev], nbytes));
        pu_gpuErrorCheck(pu_gpuDeviceSynchronize());
        sleep(2.0);
        LogTimeTakenOnDevice(time_local);
        LogGPUStatistics(sgpu);
    }
    LogTimeTaken(tgpumem);
#endif

#ifdef _MPI
    MPI_Finalize();
#endif 

}
