cmake_minimum_required(VERSION 3.22..3.28)
project(diffwoodcore)

include(CheckLanguage)
check_language(CUDA)

if(CMAKE_CUDA_COMPILER)
    enable_language(CXX CUDA)
    set(DIFFWOOD_CUDA ON)
else()
    enable_language(CXX)
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


find_package(Eigen3 3.4 REQUIRED NO_MODULE)

add_subdirectory(src)
target_compile_options(diffwood PRIVATE -fPIC)

add_executable(test src/test.cpp)
target_include_directories(test PUBLIC src)
target_link_libraries(test PUBLIC Eigen3::Eigen diffwood)




find_package(Python COMPONENTS Interpreter Development REQUIRED)
add_subdirectory(ext/nanobind)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_CURRENT_LIST_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_CURRENT_LIST_DIR})

nanobind_add_module(_diffwoodcore NOMINSIZE src/main.cpp)
target_include_directories(_diffwoodcore PUBLIC src)
target_link_libraries(_diffwoodcore PUBLIC Eigen3::Eigen diffwood)

add_dependencies(test _diffwoodcore)


