cmake_minimum_required(VERSION 3.5)
project(tangentsky)
enable_testing()
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX
      ${CMAKE_BINARY_DIR}/install
      CACHE PATH "cmake installation directory")
endif()

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

if(EXISTS ${CMAKE_SOURCE_DIR}/build_tooling/cmake)
  list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/build_tooling/cmake)
endif()
# NOTE(josh): kitware documentation says that this is already the case, however
# that does not seem to be true.
list(APPEND CMAKE_MODULE_PATH /usr/share/cmake/Modules)
include(tangent)

include_directories(${CMAKE_SOURCE_DIR})

set(CMAKE_CXX_STANDARD "11")
set(CMAKE_C_STANDARD "99")
# NOTE(josh): needed to workaround some issue. I forgot what exactly.
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -rdynamic")

# Allow us to import/execute modules directly from the source tree
set(ENV{PYTHONPATH} ${CMAKE_SOURCE_DIR})
set(CTEST_ENVIRONMENT "PYTHONPATH=${CMAKE_SOURCE_DIR}")

add_compile_options(-Wall -Werror)

if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  if(CMAKE_CXX_COMPILE_VERSION VERSION_GREATER 5.9.99)
    add_compile_options(
      -Wimplicit-fallthrough
      "--system-header-prefix=${CMAKE_SOURCE_DIR}/third_party")
  endif()
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  if(CMAKE_CXX_COMPILE_VERSION VERSION_GREATER 6.9.9)
    add_compile_options(-Wimplicit-fallthrough)
  endif()
endif()

glob_subdirs()
