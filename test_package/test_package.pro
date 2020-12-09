 CONFIG += conan_basic_setup
 include($$OUT_PWD/../conanbuildinfo.pri)

SOURCES += test_package.cpp

HEADERS += greeter.h

QT -= gui

CONFIG += console