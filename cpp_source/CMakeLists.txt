cmake_minimum_required(VERSION 3.10)
project(structured_valuation)
set(CMAKE_PREFIX_PATH "C:\\Users\\smbserver\\miniconda3\\Lib\\site-packages\\pybind11")
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 REQUIRED)

set(TOP_DIR ..)
# 添加子目录
add_subdirectory(structured_valuation)

# 加入cpp文件
pybind11_add_module(example SHARED structured_valuation/cmb_shark_fin.cpp)

# 设置输出文件后缀名为 .pyd (Windows) 或 .so (Linux/Mac)
set_target_properties(example PROPERTIES SUFFIX ".pyd")

# 添加包含目录
include_directories(pybind11/include)

# 查找Python库
find_package(Python3 COMPONENTS Development REQUIRED)
include_directories(${Python3_INCLUDE_DIRS})
target_link_libraries(example PRIVATE ${Python3_LIBRARIES})
