/*! \file profile_util_api.h
 *  \brief this file contains all definitions that provide useful API to library calls.
 */

#ifndef _PROFILE_UTIL_API
#define _PROFILE_UTIL_API

/// \def logger utility definitions 
//@{
#define _where_calling_from "@"<<__func__<<" "<<profiling_util::__extract_filename(__FILE__)<<":L"<<std::to_string(__LINE__)<<" "
#define _when_calling_from "("<<profiling_util::__when()<<") : "
#ifdef _MPI 
#define _MPI_calling_rank "["<<std::setw(5) << std::setfill('0')<<profiling_util::__comm_rank<<"] "<<std::setw(0)
#define _log_header _MPI_calling_rank<<_where_calling_from<<_when_calling_from
#else 
#define _log_header _where_calling_from<<_when_calling_from
#endif

//@}

/// \def gerenal logging  
//@{
#ifdef _MPI
#define MPISetLoggingComm(comm) {profiling_util::__comm = comm; MPI_Comm_rank(profiling_util::__comm, &profiling_util::__comm_rank);}
#endif
#define Logger(logger) logger<<_log_header
#define Log() std::cout<<_log_header
#define LogErr() std::cerr<<_log_header

#ifdef _OPENMP
#ifdef _MPI 
#define LOGGING() shared(profiling_util::__comm, profiling_util::__comm_rank, std::cout)
#else 
#define LOGGING() shared(std::cout)
#endif
#endif
//@}

/// \defgroup LogVersion
/// report information about utility version
//@{
/// report version 
#define LogVersion() Log()<<profiling_util::__version()<<std::endl;
#ifdef _MPI
#define MPILog0Version() if(profiling_util::__comm_rank == 0) Log()<<profiling_util::__version()<<std::endl;
#endif
//@}

/// \defgroup LogAffinity
/// Log thread affinity and parallelism either to std or an ostream
//@{
#define LogParallelAPI() Log()<<"\n"<<profiling_util::ReportParallelAPI()<<std::endl;
#define LogBinding() Log()<<"\n"<<profiling_util::ReportBinding()<<std::endl;
#define LogThreadAffinity() {auto __s = profiling_util::ReportThreadAffinity(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__)); Log()<<__s;}
#define LoggerThreadAffinity(logger) {auto __s = <<profiling_util::ReportThreadAffinity(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__)); Logger(logger)<<__s;}
#ifdef _MPI
#define MPILog0ThreadAffinity() if(profiling_util::__comm_rank == 0) LogThreadAffinity();
#define MPILogger0ThreadAffinity(logger) if(profiling_util::__comm_rank == 0) LogThreadAffinity(logger);
#define MPILogThreadAffinity() {auto __s = profiling_util::MPIReportThreadAffinity(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__),  profiling_util::__comm); Log()<<__s;}
#define MPILoggerThreadAffinity(logger) {auto __s = profiling_util::MPIReportThreadAffinity(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__), profiling_util::__comm); Logger(logger)<<__s;}
#define MPILog0ParallelAPI() if(profiling_util::__comm_rank == 0) Log()<<"\n"<<profiling_util::ReportParallelAPI()<<std::endl;
#define MPILog0Binding() {auto s = profiling_util::ReportBinding(); if (profiling_util::__comm_rank == 0)Log()<<"\n"<<s<<std::endl;}
#endif
//@}

/// \defgroup LogMem
/// Log memory usage either to std or an ostream
//@{
#define LogMemUsage() Log()<<profiling_util::ReportMemUsage(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LoggerMemUsage(logger) Logger(logger)<<profiling_util::ReportMemUsage(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;

#ifdef _MPI
#define MPILogMemUsage() Log()<<profiling_util::ReportMemUsage(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define MPILoggerMemUsage(logger) Logger(logger)<<profiling_util::ReportMemUsage(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define MPILog0NodeMemUsage() {auto __s=profiling_util::MPIReportNodeMemUsage(profiling_util::__comm, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__)); if (profiling_util::__comm_rank == 0) {Log()<<__s<<std::endl;}}
#define MPILogger0NodeMemUsage(logger) {auto __s=profiling_util::MPIReportNodeMemUsage(profiling_util::__comm, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__)); int __comm_rank; if (profiling_util::__comm_rank == 0) {Logger(logger)<<__s<<std::endl;}}
#endif

#define LogSystemMem() std::cout<<profiling_util::ReportSystemMem(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LoggerSystemMem(logger) logger<<profiling_util::ReportSystemMem(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;

#ifdef _MPI
#define MPILogSystemMem() Log()<<profiling_util::ReportSystemMem(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define MPILoggerSystemMem(logger) Logger(logger)<<profiling_util::ReportSystemMem(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define MPILog0NodeSystemMem() {auto __s=profiling_util::MPIReportNodeSystemMem(profiling_util::__comm, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__));if (profiling_util::__comm_rank == 0){Log()<<__s<<std::endl;}}
#define MPILogger0NodeSystemMem(logger) {auto __s = profiling_util::MPIReportNodeSystemMem(profiling_util::__comm, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__));if (profiling_util::__comm_rank == 0) {Logger(logger)<<__s<<std::endl;}}
#endif
//@}


/// \defgroup LogTime
/// Log time taken either to std or an ostream
//@{
#define LogTimeTaken(timer) Log()<<profiling_util::ReportTimeTaken(timer, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LoggerTimeTaken(logger,timer) Logger(logger)<<profiling_util::ReportTimeTaken(timer,__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LogTimeTakenOnDevice(timer) Log()<<profiling_util::ReportTimeTakenOnDevice(timer, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LoggerTimeTakenOnDevice(logger,timer) Logger(logger)<<profiling_util::ReportTimeTakenOnDevice(timer,__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#ifdef _MPI
#define MPILogTimeTaken(timer) Log()<<profiling_util::ReportTimeTaken(timer, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define MPILoggerTimeTaken(logger,timer) Logger(logger)<<profiling_util::ReportTimeTaken(timer,__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define MPILogTimeTakenOnDevice(timer) Log()<<profiling_util::ReportTimeTakenOnDevice(timer, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define MPILoggerTimeTakenOnDevice(logger,timer) Logger(logger)<<profiling_util::ReportTimeTakenOnDevice(timer,__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#endif 
#define NewTimer() profiling_util::Timer(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__));
#define NewTimerHostOnly() profiling_util::Timer(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__), false);

#define NewSampler(t) profiling_util::StateSampler(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__), true, t);
#define NewSamplerHostOnly(t) profiling_util::StateSampler(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__), false, t);
//@}

/// \defgroup LogUsage
/// Log usage statistics either to std or an ostream
//@{
#define LogCPUUsage(sampler) Log()<<profiling_util::ReportCPUUsage(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LoggerCPUUsage(logger,timer) Logger(logger)<<profiling_util::ReportCPUUsage(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#ifdef _MPI
#define MPILogCPUUsage(sampler) Log()<<profiling_util::ReportCPUUsage(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define MPILoggerCPUUsage(logger,timer) Logger(logger)<<profiling_util::profiling_util::ReportCPUUsage(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#endif 

#ifdef _GPU
#define LogGPUUsage(sampler) Log()<<profiling_util::ReportGPUUsage(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LoggerGPUUsage(logger,sampler) Logger(logger)<<profiling_util::ReportGPUUsage(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LogGPUEnergy(sampler) Log()<<profiling_util::ReportGPUEnergy(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LoggerGPUEnergy(logger,sampler) Logger(logger)<<profiling_util::ReportGPUEnergy(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LogGPUMem(sampler) Log()<<profiling_util::ReportGPUMem(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LoggerGPUMem(logger,sampler) Logger(logger)<<profiling_util::ReportGPUMem(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LogGPUMemUsage(sampler) Log()<<profiling_util::ReportGPUMemUsage(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LoggerGPUMemUsage(logger,sampler) Logger(logger)<<profiling_util::ReportGPUMemUsage(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LogGPUStatistics(sampler) Log()<<profiling_util::ReportGPUStatistics(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#define LoggerGPUStatistics(logger,sampler) Logger(logger)<<profiling_util::ReportGPUStatistics(sampler, __func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__))<<std::endl;
#endif

#define NewComputeSampler(t) profiling_util::ComputeSampler(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__), t, true);
#define NewComputeSamplerHostOnly(t) profiling_util::ComputeSampler(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__), t, false);

#define NewSTraceSampler(t) profiling_util::STraceSampler(__func__, profiling_util::__extract_filename(__FILE__), std::to_string(__LINE__), true, t);
//@}

#endif
