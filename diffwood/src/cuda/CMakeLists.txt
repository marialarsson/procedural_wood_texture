cmake_minimum_required(VERSION 3.22...3.28)
project(cudiffwood)

enable_language(CUDA)
set(CMAKE_CUDA_STANDARD 14)

find_package(Eigen3 3.4 REQUIRED NO_MODULE)

set(SRC common.cuh
        add.cu)

add_library(cudiffwood ${SRC})
target_include_directories(cudiffwood PRIVATE ${CMAKE_CURRENT_LIST_DIR}/..)
target_link_libraries(cudiffwood PRIVATE Eigen3::Eigen)
target_compile_definitions(cudiffwood PRIVATE COMPILE_WITH_CUDA)
set_property(TARGET cudiffwood PROPERTY CUDA_SEPARABLE_COMPILATION ON)

