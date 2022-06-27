cmake_minimum_required(VERSION 3.16.3)
project(erf_fortran_python_matlab Fortran)

add_library(lib cerf_lib.f90)
add_executable(cerf cerf.f90)
target_link_libraries(cerf lib)
