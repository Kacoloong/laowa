cmake_minimum_required(VERSION 3.22)

set(GUROBI_ROOT /opt/gurobi1200/linux64)
set(GUROBI_INCLUDE_DIR ${GUROBI_ROOT}/include)
set(GUROBI_LIB_DIR ${GUROBI_ROOT}/lib)

# 包含 gurobi 的头文件
include_directories(${GUROBI_INCLUDE_DIR})

# 链接 gurobi 库
link_directories(${GUROBI_LIB_DIR})

project(ImpossibleDifferential)

set(CMAKE_CXX_STANDARD 20)
# 添加可执行文件
add_executable(ImpossibleDifferential
        main.cpp
        toolkit.h
)
# 链接 Gurobi 所需的库文件
target_link_libraries(ImpossibleDifferential
        gurobi_c++
        gurobi120
)