cmake_minimum_required(VERSION 3.1.0)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(CTest)
set(BUILD_TESTING ON)

# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Instruct CMake to run moc automatically when needed
set(CMAKE_AUTOMOC ON)
# Create code from a list of Qt designer ui files
set(CMAKE_AUTOUIC ON)

# Find the QtCore library
find_package(Qt5Core CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp greeter.h)
target_link_libraries(${PROJECT_NAME} Qt5::Core)

add_test(NAME test_package
         COMMAND "$<TARGET_FILE:test_package>")

# configure_file(${CMAKE_CURRENT_BINARY_DIR}/qt.conf ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/qt.conf COPYONLY)

option(MY_TEST_QTWEBENGINE "test qtwebengine if ON.")
if(MY_TEST_QTWEBENGINE)
    find_package(Qt5WebEngine CONFIG REQUIRED)
    add_executable(test_qtwebengine test_qtwebengine.cpp)
    target_link_libraries(test_qtwebengine Qt5::WebEngine)
    add_test(NAME test_qtwebengine
             COMMAND "$<TARGET_FILE:test_qtwebengine>")
endif()
