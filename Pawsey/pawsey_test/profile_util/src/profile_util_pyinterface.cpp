/*! \file profile_util_pyinterface.cpp
 *  \brief Define the interface to the profile util classes and calls
*/

//possibly other stuff to include
// cfg['extra_link_args'] = ['...']
// cfg['extra_compile_args'] = ['...']
// cfg['libraries'] = ['...']
#ifdef _USING_CPPIMPORT
<%
import subprocess, shutil
def my_preprocess_script():
    # Example sed command

    shutil.copyfile("get_revision.cpp.in", "pybind11_git_revision.cpp")
    #sed_command = ['sed', '-i', '', 's//new_text/g', "pybind11_git_revision.cpp"]
    #subprocess.run(sed_command, check=True)

cfg['preprocess_script'] = my_preprocess_script
cfg['compiler_args'] = ['-std=c++20', '-O3']
cfg['include_dirs'] = ['../include/']
cfg['sources'] = ['profile_util.cpp', 'mem_util.cpp', 'thread_affinity_util.cpp', 'time_util.cpp',  'pybind11_git_revision.cpp']
cfg['dependencies'] = ['../include/profile_util.h', '../include/profile_util_gpu.h']
cfg['parallel'] = True
setup_pybind11(cfg)
%>
#endif

#include "profile_util.h"
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace std;
using namespace profiling_util;

/// @brief python module for profile_util
/// @param py_profile_util name of python library to import
/// @param m python module class
PYBIND11_MODULE(py_profile_util, m) {
    /// @brief Python Timer class API
    py::class_<Timer>(m, "Timer")
        .def(py::init<const std::string&, const std::string&, const std::string&, bool>())
        .def("get_use_device", &Timer::get_use_device)
        .def("get", &Timer::get)
        .def("get_creation", &Timer::get_creation)
#if defined(_GPU)
        .def("get_on_device", &Timer::get_on_device)
        .def("get_device_swap_info", &Timer::get_device_swap_info)
#endif
        .def("set_ref", &Timer::set_ref)
        .def("get_ref", &Timer::get_ref);
    
    m.def("ReportTimeTaken", &ReportTimeTaken, 
        "Reports the time taken (on host) between creation of timer and when/where this is called"
        );
#if defined(_GPU)
    m.def("ReportTimeTakenOnDevice", &ReportTimeTakenOnDevice, 
        "Reports the time taken (on device) between creation of timer and when/where this is called"
        );
#endif

    /// @brief Python Timer class API
    //@{
    py::class_<ComputeSampler>(m, "ComputeSampler")
        .def(py::init<const std::string &, const std::string &, const std::string &, float , bool , bool>())
        .def("GetCPUUsageFname", &ComputeSampler::GetCPUUsageFname)
        .def("GetCPUEnergyFname", &ComputeSampler::GetCPUEnergyFname)
#ifdef _GPU 
        .def("GetGPUUsageFname", &ComputeSampler::GetGPUUsageFname)
        .def("GetGPUEnergyFname", &ComputeSampler::GetGPUEnergyFname)
        .def("GetGPUMemUsageFname", &ComputeSampler::GetGPUMemUsageFname)
        .def("GetGPUMemFname", &ComputeSampler::GetGPUMemFname)
#endif
        .def("GetNumDevices", &ComputeSampler::GetNumDevices);
    
    m.def("ReportCPUUsage", &ReportCPUUsage, 
        "Reports the usage of CPUs between creation of sampler and when/where this is called."
        );
#if defined(_GPU)
    m.def("ReportGPUUsage", &ReportGPUUsage, 
        "Reports the usage of GPU between creation of sampler and when/where this is called."
        );
    m.def("ReportGPUEnergy", &ReportGPUEnergy, 
        "Reports the power and energy consumed of GPU between creation of sampler and when/where this is called."
        );
    m.def("ReportGPUMem", &ReportGPUMem, 
        "Reports the GPU memory used in MiB between creation of sampler and when/where this is called."
        );
    m.def("ReportGPUMemUsage", &ReportGPUMemUsage, 
        "Reports the GPU memory used in % between creation of sampler and when/where this is called."
        );
    m.def("ReportGPUStatistics", &ReportStatistics, 
        "Reports the GPU statistics (usage, energy, etc) between creation of sampler and when/where this is called."
        );
#endif
    //@}

    /// @defgroup Python_API_Thread_affinity
    //@{
    m.def("cpuset_to_cstr", &cpuset_to_cstr);
    m.def("MPICallingRank", &MPICallingRank, 
        "A function that returns string of calling mpi rank", py::arg("rank"));
    m.def("ReportParallelAPI", &ReportParallelAPI, 
        "Reports all the parallel APIs being used");
    m.def("ReportBinding", &ReportBinding, 
        "Reports the core and gpu binding");
    m.def("ReportThreadAffinity", &ReportThreadAffinity, 
        "Reports the core affinity for a given calling thread");
#ifdef _MPI
    m.def("MPIReportThreadAffinity", &MPIReportThreadAffinity, 
        "Reports the MPI aware core affinity for a given calling thread");
#endif
    //@}

    /// @defgroup Python_API_Mem_usage
    //{@
    py::class_<memory_usage>(m, "memory_usage");
    py::class_<sys_memory_stats>(m, "sys_memory_stats");
    m.def("GetMemUsage", 
        py::overload_cast<const std::string &, const std::string &, const std::string &>(&GetMemUsage),
        "Return the memory used by the process" 
        );
    m.def("GetMemUsage", 
        py::overload_cast<const memory_usage &, const std::string &, const std::string &, const std::string &>(&GetMemUsage),
        "Returns the memory used by the process relative to a memory usage point" 
        );
    m.def("ReportMemUsage", 
        py::overload_cast<const std::string &, const std::string &, const std::string &>(&ReportMemUsage),
        "Reports the memory used by the process" 
        );
    m.def("ReportMemUsage", 
        py::overload_cast<const memory_usage &, const std::string &, const std::string &, const std::string &>(&ReportMemUsage),
        "Reports the memory used by the process relative to a memory usage point" 
        );
    m.def("ReportSystemMem", 
        py::overload_cast<const std::string &, const std::string &, const std::string &>(&ReportSystemMem), 
        "Reports the memory state of the node" 
    );
    m.def("ReportSystemMem", 
        py::overload_cast<const sys_memory_stats &, const std::string &, const std::string &, const std::string &>(&ReportSystemMem), 
        "Reports the memory state of the node relative to a memory usage point" 
    );
#ifdef _MPI 
    m.def("MPIReportNodeMemUsage",  
        py::overload_cast<MPI_Comm &, const std::string &, const std::string &, const std::string &>(&MPIReportMemUsage),
        "Reports the memory used by a MPI process" 
    );
    m.def("MPIReportNodeSystemMem", 
        py::overload_cast<MPI_Comm &, const std::string &, const std::string &, const std::string &>(&MPIReportSystemMem), 
        "Reports the memory state of all nodes in the MPI comm" 
    );
#endif
    //@}
}

