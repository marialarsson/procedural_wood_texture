cmake_minimum_required(VERSION 3.22..3.28)
project(diffwood)

if(DIFFWOOD_CUDA)
    enable_language(CXX CUDA)
else()
    enable_language(CXX)
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Eigen3 3.4 REQUIRED NO_MODULE)

set(SRC common.h
        thread.h
        noise.h
        noise.cpp
        diffwood.h
        diffwood.cpp)

add_library(diffwood ${SRC})
target_link_libraries(diffwood PUBLIC Eigen3::Eigen)

if (DIFFWOOD_CUDA)
    add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/cuda)
    target_compile_options(cudiffwood PRIVATE -fPIC)
    target_link_libraries(diffwood PRIVATE cudiffwood)
    target_compile_definitions(diffwood PRIVATE DIFFWOOD_CUDA)
    set_property(TARGET diffwood PROPERTY CUDA_SEPARABLE_COMPILATION ON)
endif()


