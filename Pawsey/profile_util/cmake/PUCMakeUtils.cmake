#
# How we find MPI and set it up
#
macro(pu_find_mpi)
    message("MPI enabled, finding MPI ... ")
    find_package(MPI)
    if (MPI_FOUND)
        list(APPEND PU_INCLUDE_DIRS ${MPI_CXX_INCLUDE_PATH})
        list(APPEND PU_LIBS ${MPI_CXX_LIBRARIES})
        list(APPEND PU_CXX_FLAGS ${MPI_CXX_FLAGS})
        list(APPEND PU_LINK_FLAGS ${MPI_CXX_FLAGS})
        list(APPEND PU_DEFINES "_MPI")
        set(PU_HAS_MPI Yes)
    else()
        message(SEND_ERROR "MPI enabled but not found. Please check configuration or disable MPI")
    endif()
endmacro()

macro(pu_find_openmp)
    message("OpenMP enabled, finding OpenMP ... ")
    find_package(OpenMP)
    #FindOpenMP()
    if (OpenMP_FOUND)
        list(APPEND PU_CXX_FLAGS ${OpenMP_CXX_FLAGS})
        list(APPEND PU_LINK_FLAGS ${OpenMP_CXX_FLAGS})
        #list(APPEND PU_DEFINES ${_OPENMP})
        set(PU_HAS_OPENMP Yes)
    else()
        message(SEND_ERROR "OpenMP enabled but not found. Please check configuration or disable OpenMP")
    endif()
endmacro()

macro(pu_find_hip)
    # Find hip
    message("HIP enabled, finding HIP ... ")
    find_package(HIP)
    if (HIP_FOUND)
        # Link with HIP
        enable_language(HIP)
        if(NOT DEFINED CMAKE_HIP_STANDARD)
            set(CMAKE_HIP_STANDARD 17)
            set(CMAKE_HIP_STANDARD_REQUIRED ON)
        endif()
        list(APPEND PU_DEFINES "_HIP")
        set(PU_HAS_HIP Yes)
        add_compile_options("-fPIE")
        target_link_libraries(hip::device)
        if (ENABLE_HIP_AMD)
            message("Using AMD HIP ")
            add_definitions("-D__HIP_PLATFORM_AMD__")
            set(GPU_TARGETS "gfx90a" CACHE STRING "GPU targets to compile for")
        endif()
    else()
        message(SEND_ERROR "HIP enabled but not found. Please check configuration or disable HIP")
    endif()
endmacro()

macro(pu_find_cuda)
    # Find hip
    message(STATUS "CUDA enabled, finding CUDA ... ")
    find_package(CUDA)
    if (CUDA_FOUND)
        enable_language(CUDA)
        list(APPEND PU_DEFINES "_CUDA")
        set(PU_HAS_CUDA Yes)
        if(NOT DEFINED CMAKE_CUDA_STANDARD)
            set(CMAKE_CUDA_STANDARD 17)
            set(CMAKE_CUDA_STANDARD_REQUIRED ON)
        endif()
    else()
        message(SEND_ERROR "CUDA enabled but not found. Please check configuration or disable CUDA")
    endif()
endmacro()

macro(pu_find_pybind)
    find_package(Python COMPONENTS Interpreter Development)
    find_package(pybind11 CONFIG REQUIRED)
    set(PYBIND11_FINDPYTHON ON)
    # # pybind11 method:
    # pybind11_add_module(MyModule1 src1.cpp)

    # # Python method:
    # Python_add_library(MyModule2 src2.cpp)
    # target_link_libraries(MyModule2 PUBLIC pybind11::headers)
    # set_target_properties(MyModule2 PROPERTIES
    #                                 INTERPROCEDURAL_OPTIMIZATION ON
    #                                 CXX_VISIBILITY_PRESET ON
    #                                 VISIBILITY_INLINES_HIDDEN ON)
endmacro()

macro(pu_mpi)
    set(PU_HAS_MPI No)
    if (PU_ENABLE_MPI)
        pu_find_mpi()
    endif()
endmacro()

macro(pu_openmp)
    set(PU_HAS_OPENMP No)
    if (PU_ENABLE_OPENMP)
        pu_find_openmp()
    endif()
endmacro()

macro(pu_hip)
    set(PU_HAS_HIP No)
    if (PU_ENABLE_HIP)
        pu_find_hip()
    endif()
endmacro()

macro(pu_cuda)
    set(PU_HAS_CUDA No)
    if (PU_ENABLE_CUDA)
        pu_find_cuda()
    endif()
endmacro()

macro(pu_pybind)
    if (PU_ENABLE_PYTHON_INTERFACE)
        pu_find_pybind()
    endif()
endmacro()

macro(pu_report feature)

    # Output feature name and underscore it in the next line
    message("\n${feature}")
    string(REGEX REPLACE "." "-" _underscores ${feature})
    message("${_underscores}\n")

    set(_args "${ARGN}")
    list(LENGTH _args _nargs)
    math(EXPR _nargs "${_nargs} - 1")
    foreach(_idx RANGE 0 ${_nargs} 2)
        # Items in the list come with a message first, then the variable name
        list(GET _args ${_idx} _msg)
        math(EXPR _idx2 "${_idx} + 1")
        list(GET _args ${_idx2} _varname)

        # We try to keep things up to 80 cols
        string(LENGTH ${_msg} _len)
        math(EXPR _nspaces "75 - ${_len}")
        string(RANDOM LENGTH ${_nspaces} _spaces)
        string(REGEX REPLACE "." " " _spaces "${_spaces}")
        string(CONCAT _msg "${_msg}" ${_spaces})
        message(" ${_msg} ${PU_HAS_${_varname}}")
    endforeach()
endmacro()

#
# Some useful utils
#

#
# list values as bullet points
#
function(list_to_bulletpoints result)
    list(REMOVE_AT ARGV 0)
    set(temp "")
    foreach(item ${ARGV})
        set(temp "${temp}* ${item}")
    endforeach()
    set(${result} "${temp}" PARENT_SCOPE)
endfunction(list_to_bulletpoints)

#
# valid the option choosen based on allowed values
#
function(validate_option name values)
    string(TOLOWER ${${name}} needle_lower)
    string(TOUPPER ${${name}} needle_upper)
    list(FIND ${values} ${needle_lower} IDX_LOWER)
    list(FIND ${values} ${needle_upper} IDX_UPPER)
    if(${IDX_LOWER} LESS 0 AND ${IDX_UPPER} LESS 0)
        list_to_bulletpoints(POSSIBLE_VALUE_LIST ${${values}})
        message(FATAL_ERROR "\n########################################################################\n"
                            "Invalid value '${${name}}' for option ${name}\n"
                            "Possible values are : "
                            "${POSSIBLE_VALUE_LIST}"
                            "\n"
                            "########################################################################")
    endif()
endfunction(validate_option)

#
# Function to add a "doc" target, which will doxygen out the given
# list of directories
#
function(try_add_doc_target doc_dirs)
	find_program(DOXYGEN_FOUND doxygen)
	if (NOT DOXYGEN_FOUND)
		return()
	endif()

	# Create a target for each individual doc directory, then a final one
	# that depends on them all
	message("-- Adding doc target for directories: ${doc_dirs}")
	set(_dependencies "")
	set(x 1)
	foreach(_doc_dir IN ITEMS ${doc_dirs})
		add_custom_command(OUTPUT ${_doc_dir}/xml/index.xml
		                   COMMAND doxygen
		                   WORKING_DIRECTORY ${_doc_dir})
		add_custom_target(doc_${x}
		                  COMMAND doxygen
		                  WORKING_DIRECTORY ${_doc_dir})
		list(APPEND _dependencies doc_${x})
		math(EXPR x "${x} + 1")
	endforeach()
	add_custom_target(doc DEPENDS "${_dependencies}")
endfunction()

#
# - Prevent in-source builds.
# https://stackoverflow.com/questions/1208681/with-cmake-how-would-you-disable-in-source-builds/
#
macro(prevent_in_source_builds)
    # make sure the user doesn't play dirty with symlinks
    get_filename_component(srcdir "${CMAKE_SOURCE_DIR}" REALPATH)
    get_filename_component(srcdir2 "${CMAKE_SOURCE_DIR}/.." REALPATH)
    get_filename_component(srcdir3 "${CMAKE_SOURCE_DIR}/../src" REALPATH)
    get_filename_component(bindir "${CMAKE_BINARY_DIR}" REALPATH)

    # disallow in-source builds
    if("${srcdir}" STREQUAL "${bindir}" OR "${srcdir2}" STREQUAL "${bindir}" OR "${srcdir3}" STREQUAL "${bindir}")
        message(FATAL_ERROR "\
            CMake must not to be run in the source directory. 
            Rather create a dedicated build directory and run CMake there. 
            To clean up after this aborted in-place compilation:
            rm -r CMakeCache.txt CMakeFiles
        ")
    endif()
endmacro()

#
# set the default build and also store the compilation flags
# as a string based on the currently choosen flags
#
macro(my_set_build_type)
	set(default_build_type "Release")
	if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
		message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
		set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
			STRING "Choose the type of build." FORCE)
		# Set the possible values of build type for cmake-gui
		set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
			"Debug" "Release" "MinSizeRel" "RelWithDebInfo")
	endif()
	#set(ACTIVE_COMPILE_OPTIONS )
endmacro()

macro(enable_santizer_option)
    set(ENABLE_SANITIZER "none" CACHE STRING "Select a code sanitizer option (none (default), address, leak, thread, undefined)")
    mark_as_advanced(ENABLE_SANITIZER)
    set(ENABLE_SANITIZER_VALUES none address leak thread undefined)
    set_property(CACHE ENABLE_SANITIZER PROPERTY STRINGS ${ENABLE_SANITIZER_VALUES})
    validate_option(ENABLE_SANITIZER ENABLE_SANITIZER_VALUES)
    string(TOLOWER ${ENABLE_SANITIZER} ENABLE_SANITIZER)
endmacro()

function(sanitizer_options mytarget)
    if(NOT ENABLE_SANITIZER STREQUAL "none")
        if((${CMAKE_CXX_COMPILER_ID} STREQUAL "GNU") OR (${CMAKE_CXX_COMPILER_ID} STREQUAL "Clang"))
            target_compile_options(${mytarget} PUBLIC -fsanitize=${ENABLE_SANITIZER})
            target_link_options(${mytarget} PUBLIC -fsanitize=${ENABLE_SANITIZER})
        else()
            message(WARNING "ENABLE_SANITIZER option not supported by ${CMAKE_CXX_COMPILER_ID} compilers. Ignoring.")
            set(ENABLE_SANITIZER "none")
        endif()
    endif()
endfunction()

#run some macros automatically
prevent_in_source_builds()
my_set_build_type()
enable_santizer_option()
