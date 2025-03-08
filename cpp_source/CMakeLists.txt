cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 17)

project(cmb_structured_valuation)
set(PYTHON_TARGET_VER 3.9)
# TODO: YOU MUST CHANGE YOUR PATH CORRECTLY
set(Python3_ROOT_DIR "C:/Users/Administrator/miniconda3/envs/py9")
set(CMAKE_PREFIX_PATH "C:/Users/Administrator/miniconda3/envs/py9/lib/site-packages/pybind11/share/cmake/pybind11")
# TODO: YOU NEED TO ADD include FOLDER INTO YOUR PATH
set(Python3_INCLUDE_DIR "C:/Users/Administrator/miniconda3/envs/py9/include")
set(Python3_LIBRARY "C:/Users/Administrator/miniconda3/envs/py9/libs/python39.lib")
set(Python3_EXECUTABLE "C:/Users/Administrator/miniconda3/envs/py9/python.exe")
set(TOP_DIR ..)
# method from stackoverflow
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static")

# Set policy CMP0148
cmake_policy(SET CMP0148 NEW)

# Enable PYBIND11_FINDPYTHON
set(PYBIND11_FINDPYTHON ON)

message(STATUS "pybind11 include directories: ${pybind11_INCLUDE_DIRS}")
include_directories(${pybind11_INCLUDE_DIRS})

find_package(Python3 COMPONENTS Development REQUIRED)
find_package(pybind11 REQUIRED)

# Add cpp file
pybind11_add_module(cmb_structured_valuation MODULE cmb_structured_valuation.cpp)

# Set output file suffix to .pyd (Windows) or .so (Linux/Mac)
if (WIN32)
    set_target_properties(cmb_structured_valuation PROPERTIES SUFFIX ".pyd")
else()
    set_target_properties(cmb_structured_valuation PROPERTIES SUFFIX ".so")
endif()

# Output path to debug
message(STATUS "Python3 Interpreter: ${Python3_EXECUTABLE}")
message(STATUS "Python3 Includes: ${Python3_INCLUDE_DIR}")
message(STATUS "Python3 Library: ${Python3_LIBRARY}")

# Add include directories
include_directories("C:/Users/Administrator/miniconda3/envs/py9/Lib/site-packages/pybind11/include")
include_directories(${Python3_INCLUDE_DIR})

# Link against Python libraries
target_link_libraries(cmb_structured_valuation PRIVATE Python3::Python)

# Check if required components are found
if(NOT Python3_EXECUTABLE OR NOT Python3_INCLUDE_DIR OR NOT Python3_LIBRARY)
    message(FATAL_ERROR "Python3 components not found.")
endif()