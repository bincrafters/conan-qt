cmake_minimum_required(VERSION 3.1.0)
project(test_package)


# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Instruct CMake to run moc automatically when needed
set(CMAKE_AUTOMOC ON)
# Instruct CMake to run rcc automatically when needed
set (CMAKE_AUTORCC ON)
# Create code from a list of Qt designer ui files
set(CMAKE_AUTOUIC ON)

# Find the QtCore library
find_package(Qt5Core CONFIG REQUIRED)

# Make sure resource files work
qt5_add_resources(TEST_RESOURCES test.qrc)

add_executable(${PROJECT_NAME} test_package.cpp greeter.h ${TEST_RESOURCES})
target_link_libraries(${PROJECT_NAME} Qt5::Core)

# configure_file(${CMAKE_CURRENT_BINARY_DIR}/qt.conf ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/qt.conf COPYONLY)
