/*! \file time_util.cpp
 *  \brief Get timing
 */

#include "profile_util.h"

namespace profiling_util {
    std::string __extract_filename(std::string fullpath) 
    { 
        auto lastSlashPos = fullpath.find_last_of('/');
        return fullpath.substr(lastSlashPos + 1);
    };

    std::string __when(){
        auto log_time = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        std::string whenbuff=std::ctime(&log_time);
        whenbuff.erase(std::find(whenbuff.begin(), whenbuff.end(), '\n'), whenbuff.end());
        return whenbuff;
    }
    std::string __version(){
        std::string version= "Version: ";
        version+= __PU_VERSION__;
        version+=", git:" + profiling_util::git_sha1();
        return version; 
    }
    template std::tuple<double, double, double, double>get_stats(std::vector<double> &input, unsigned int offset, unsigned int stride);
    template std::tuple<float, float, float, float>get_stats(std::vector<float> &input, unsigned int offset, unsigned int stride);

    #ifdef _MPI
    static bool _PU_USING_MPI=true;
    #endif
    #ifdef _HIP
    static bool _PU_USING_HIP=true;
    #endif
    #ifdef _CUDA
    static bool _PU_USING_CUDA=true;
    #endif
    #ifdef _OPENMP
    static bool _PU_USING_OPENMP=true;
    #endif
}

