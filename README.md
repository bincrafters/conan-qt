[![Download](https://api.bintray.com/packages/bincrafters/public-conan/qt%3Abincrafters/images/download.svg) ](https://bintray.com/bincrafters/public-conan/qt%3Abincrafters/_latestVersion)
[![Build Status Travis](https://travis-ci.com/bincrafters/conan-qt.svg?branch=stable%2F5.12.0)](https://travis-ci.com/bincrafters/conan-qt)
[![Build Status Azure](https://dev.azure.com/bincrafters/packages/_apis/build/status/bincrafters.conan-qt?branchName=stable%2F5.12.0)](https://dev.azure.com/bincrafters/packages/_build)
[![Build Status AppVeyor](https://ci.appveyor.com/api/projects/status/github/bincrafters/conan-qt?branch=stable%2F5.12.0&svg=true)](https://ci.appveyor.com/project/bincrafters/conan-qt)

## Conan package recipe for [*qt*](https://www.qt.io)

Qt is a cross-platform framework for graphical user interfaces.

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/bincrafters/public-conan/qt%3Abincrafters).


## Issues

If you wish to report an issue or make a request for a package, please do so here:

[Issues Tracker](https://github.com/bincrafters/community/issues)


## For Users

### Basic setup

    $ conan install qt/5.12.0@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    qt/5.12.0@bincrafters/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.


## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create . bincrafters/stable


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| shared      | True |  [True, False] |
| commercial      | False |  [True, False] |
| opengl      | desktop |  ['no', 'es2', 'desktop', 'dynamic'] |
| openssl      | True |  [True, False] |
| with_pcre2      | True |  [True, False] |
| with_doubleconversion      | True |  [True, False] |
| with_freetype      | True |  [True, False] |
| with_harfbuzz      | True |  [True, False] |
| with_libjpeg      | True |  [True, False] |
| with_libpng      | True |  [True, False] |
| with_sqlite3      | True |  [True, False] |
| with_pq      | True |  [True, False] |
| with_odbc      | True |  [True, False] |
| with_sdl2      | True |  [True, False] |
| with_libalsa      | True |  [True, False] |
| with_openal      | True |  [True, False] |
| GUI      | True |  [True, False] |
| widgets      | True |  [True, False] |
| device      |  |  ANY |
| cross_compile      |  |  ANY |
| config      |  |  ANY |
| qtbase      | False |  [True, False] |
| qtsvg      | False |  [True, False] |
| qtdeclarative      | False |  [True, False] |
| qtactiveqt      | False |  [True, False] |
| qtscript      | False |  [True, False] |
| qtmultimedia      | False |  [True, False] |
| qttools      | False |  [True, False] |
| qtxmlpatterns      | False |  [True, False] |
| qttranslations      | False |  [True, False] |
| qtdoc      | False |  [True, False] |
| qtrepotools      | False |  [True, False] |
| qtqa      | False |  [True, False] |
| qtlocation      | False |  [True, False] |
| qtsensors      | False |  [True, False] |
| qtconnectivity      | False |  [True, False] |
| qtwayland      | False |  [True, False] |
| qt3d      | False |  [True, False] |
| qtimageformats      | False |  [True, False] |
| qtgraphicaleffects      | False |  [True, False] |
| qtquickcontrols      | False |  [True, False] |
| qtserialbus      | False |  [True, False] |
| qtserialport      | False |  [True, False] |
| qtx11extras      | False |  [True, False] |
| qtmacextras      | False |  [True, False] |
| qtwinextras      | False |  [True, False] |
| qtandroidextras      | False |  [True, False] |
| qtwebsockets      | False |  [True, False] |
| qtwebchannel      | False |  [True, False] |
| qtwebengine      | False |  [True, False] |
| qtcanvas3d      | False |  [True, False] |
| qtwebview      | False |  [True, False] |
| qtquickcontrols2      | False |  [True, False] |
| qtpurchasing      | False |  [True, False] |
| qtcharts      | False |  [True, False] |
| qtdatavis3d      | False |  [True, False] |
| qtvirtualkeyboard      | False |  [True, False] |
| qtgamepad      | False |  [True, False] |
| qtscxml      | False |  [True, False] |
| qtspeech      | False |  [True, False] |
| qtnetworkauth      | False |  [True, False] |
| qtremoteobjects      | False |  [True, False] |
| qtwebglplugin      | False |  [True, False] |


## Add Remote

    $ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package qt.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/bincrafters/conan-qt/blob/stable/5.12.0/LICENSE.md)
