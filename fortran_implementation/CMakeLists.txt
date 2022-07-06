cmake_minimum_required(VERSION 3.16.3)
project(erf_fortran_python_matlab Fortran C)

set(CMAKE_Fortran_FLAGS_RELEASE "-Ofast -march=native")
set(CMAKE_CXX_FLAGS_RELEASE "-Ofast -march=native")

add_library(lib
        cerf_lib.f90
        Faddeeva.c
        faddeeva_fortran_interface.f90)

add_executable(cerf cerf.f90)
target_link_libraries(cerf lib)
