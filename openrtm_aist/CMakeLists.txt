if(NOT USE_ROSBUILD)
  include(catkin.cmake)
  return()
endif()
cmake_minimum_required(VERSION 2.4.6)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

# Set the build type.  Options are:
#  Coverage       : w/ debug symbols, w/o optimization, w/ code-coverage
#  Debug          : w/ debug symbols, w/o optimization
#  Release        : w/o debug symbols, w/ optimization
#  RelWithDebInfo : w/ debug symbols, w/ optimization
#  MinSizeRel     : w/o debug symbols, w/ optimization, stripped binaries
#set(ROS_BUILD_TYPE RelWithDebInfo)

rosbuild_init()

# Build OpenRTM
execute_process(COMMAND omniidl -V
                RESULT_VARIABLE have_omniidl)
if(NOT "${have_omniidl}" STREQUAL "0")
  message(FATAL_ERROR "CORBA compiler is not found, forget to install omniidl?")
endif()
execute_process(COMMAND cmake -E chdir ${PROJECT_SOURCE_DIR} make -f Makefile.openrtm_aist
                RESULT_VARIABLE _make_failed)
if (_make_failed)
  message(FATAL_ERROR "Build of OpenRTM C++ failed")
endif(_make_failed)

## clean
set_directory_properties(PROPERTIES ADDITIONAL_MAKE_CLEAN_FILES "${CMAKE_SOURCE_DIR}/bin;${CMAKE_SOURCE_DIR}/lib;${CMAKE_SOURCE_DIR}/etc;${CMAKE_SOURCE_DIR}/include;${CMAKE_SOURCE_DIR}/share")

rosbuild_add_rostest(test/test_openrtm_aist.test)
