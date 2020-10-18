cmake_minimum_required(VERSION 3.1.0)

set(CMAKE_CXX_STANDARD 11)

#set(CMAKE_POSITION_INDEPENDENT_CODE ON)

project(test_package)

include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_set_vs_runtime()
conan_set_libcxx()
conan_output_dirs_setup()

find_package(qt REQUIRED CONFIG)

# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Instruct CMake to run moc automatically when needed
set(CMAKE_AUTOMOC ON)
# Create code from a list of Qt designer ui files
set(CMAKE_AUTOUIC ON)

# Find the QtCore library in order to AUTOMOC, AUTOUIC and AUTORCC be enabled / works correctly
find_package(Qt5 COMPONENTS Core)

add_executable(${PROJECT_NAME} test_package.cpp greeter.h)
# Must compile with "-fPIC" since Qt was built with -reduce-relocations.
target_compile_options(${PROJECT_NAME} PRIVATE -fPIC)

target_link_libraries(${PROJECT_NAME} qt::qt)

# configure_file(${CMAKE_CURRENT_BINARY_DIR}/qt.conf ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/qt.conf COPYONLY)

message(">>>>>>>> CMAKE_VERSION ${CMAKE_VERSION}")
message(">>>>>>>> CMAKE_CXX_STANDARD_LIBRARIES ${CMAKE_CXX_STANDARD_LIBRARIES}")
