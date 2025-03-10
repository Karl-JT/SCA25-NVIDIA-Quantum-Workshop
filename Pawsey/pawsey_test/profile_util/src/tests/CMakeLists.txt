# Pawsey Supercomputing Research Centre
#
# Test building executable with profile_util library 

set(tests
    test_profile_util
)

foreach(test ${tests})
  add_executable(${test} ${test}.cpp)
  target_link_libraries(${test} profile_util ${PU_LIBS})
  if (PU_LINK_FLAGS)
    set_target_properties(${test} PROPERTIES LINK_FLAGS ${PU_LINK_FLAGS})
  endif()
endforeach()

