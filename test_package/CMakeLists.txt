cmake_minimum_required(VERSION 3.1.0)
project(test_package)

# Below lines are to fix this error:
#     error: "You must build your code with position independent code if Qt was built with -reduce-relocations. "
#     "Compile your code with -fPIC (-fPIE is not enough)."
set(CMAKE_POSITION_INDEPENDENT_CODE ${CONAN_CMAKE_POSITION_INDEPENDENT_CODE})


#include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
find_package(qt REQUIRED CONFIG)

#below macros are missing and probably unnecessary when using "find_package(qt...)"
#conan_set_vs_runtime()
#conan_set_libcxx()
#conan_output_dirs_setup()

set(CMAKE_VERBOSE_MAKEFILE TRUE)

# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Instruct CMake to run moc automatically when needed
set(CMAKE_AUTOMOC ON)
# Create code from a list of Qt designer ui files
set(CMAKE_AUTOUIC ON)

# Find the QtCore library
#find_package(Qt5Core CONFIG REQUIRED)
# "find_package(Qt5 COMPONENTS Widgets)" or "find_package(Qt5 COMPONENTS Core)" or maybe other can be used
# in order to AUTOMOC, AUTOUIC and AUTORCC be enabled / works correctly
find_package(Qt5 COMPONENTS Core)

add_executable(${PROJECT_NAME} test_package.cpp greeter.h)
#target_link_libraries(${PROJECT_NAME} Qt5::Core)
target_link_libraries(${PROJECT_NAME} qt::qt)

# configure_file(${CMAKE_CURRENT_BINARY_DIR}/qt.conf ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/qt.conf COPYONLY)

message(">>>>>>>> CMAKE_VERSION ${CMAKE_VERSION}")
message(">>>>>>>> CMAKE_CXX_STANDARD_LIBRARIES ${CMAKE_CXX_STANDARD_LIBRARIES}")
