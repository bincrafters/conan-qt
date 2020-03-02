## Package Status

| Bintray | Windows | Linux & macOS |
|:--------:|:---------:|:-----------------:|
|[![Download](https://api.bintray.com/packages/bincrafters/public-conan/qt%3Abincrafters/images/download.svg) ](https://bintray.com/bincrafters/public-conan/qt%3Abincrafters/_latestVersion)|[![Build status](https://ci.appveyor.com/api/projects/status/github/bincrafters/conan-qt?svg=true)](https://ci.appveyor.com/project/bincrafters/conan-qt)|[![Build Status](https://travis-ci.com/bincrafters/conan-qt.svg)](https://travis-ci.com/bincrafters/conan-qt)|

## Conan Information

Bincrafters packages can be found in the following public Conan repository:

[Bincrafters Public Conan Repository on Bintray](https://bintray.com/bincrafters/public-conan)

*Note: You can click the "Set Me Up" button on the Bintray page above for instructions on using packages from this repository.*


## Issues

If you wish to report an issue or make a request for a Bincrafters package, please do so here:

[Bincrafters Community Issues](https://github.com/bincrafters/community/issues)


## General Information

This git repository is managed by the Bincrafters team and holds files related to Conan.  For detailed information about Bincrafters and Conan, please visit the following resources:

[Conan Documentation](https://docs.conan.io)

[Bincrafters Technical Documentation](http://bincrafters.readthedocs.io/en/latest/)

[Bincrafters Blog](https://bincrafters.github.io)

## For users

### Basic Setup

```
conan install qt/5.14.1@bincrafters/stable
```

### Available Options
| Option                | Default   | Possible Values                        |
| ----------------------|:----------|:--------------------------------------:|
| shared                | True      |  [True, False]                         |
| commercial            | False     |  [True, False]                         |
| opengl                | "desktop" |  ["no", "es2", "desktop", "dynamic"]   |
| openssl               | True      |  [True, False]                         |
| with_pcre2            | True      |  [True, False]                         |
| with_glib             | True      |  [True, False]                         |
| with_doubleconversion | True      |  [True, False]                         |
| with_freetype         | True      |  [True, False]                         |
| with_fontconfig       | True      |  [True, False]                         |
| with_icu              | True      |  [True, False]                         |
| with_harfbuzz         | True      |  [True, False]                         |
| with_libjpeg          | True      |  [True, False]                         |
| with_libpng           | True      |  [True, False]                         |
| with_sqlite3          | True      |  [True, False]                         |
| with_mysql            | True      |  [True, False]                         |
| with_pq               | True      |  [True, False]                         |
| with_odbc             | True      |  [True, False]                         |
| with_sdl2             | True      |  [True, False]                         |
| with_libalsa          | False     |  [True, False]                         |
| with_openal           | True      |  [True, False]                         |
| with_zstd             | True      |  [True, False]                         |
| GUI                   | True      |  [True, False]                         |
| widgets               | True      |  [True, False]                         |
| device                | None      |  Any                                   |
| cross_compile         | True      |  [True, False]                         |
| sysroot               | True      |  [True, False]                         |
| config                | False     |  [True, False]                         |
| multiconfiguration    | False     |  [True, False]                         |
| qtsvg                 | False     |  [True, False]                         |
| qtdeclarative         | False     |  [True, False]                         |
| qtactiveqt            | False     |  [True, False]                         |
| qtscript              | False     |  [True, False]                         |
| qtmultimedia          | False     |  [True, False]                         |
| qttools               | False     |  [True, False]                         |
| qtxmlpatterns         | False     |  [True, False]                         |
| qttranslations        | False     |  [True, False]                         |
| qtdoc                 | False     |  [True, False]                         |
| qtrepotools           | False     |  [True, False]                         |
| qtqa                  | False     |  [True, False]                         |
| qtlocation            | False     |  [True, False]                         |
| qtsensors             | False     |  [True, False]                         |
| qtsystems             | False     |  [True, False]                         |
| qtfeedback            | False     |  [True, False]                         |
| qtdocgallery          | False     |  [True, False]                         |
| qtpim                 | False     |  [True, False]                         |
| qtconnectivity        | False     |  [True, False]                         |
| qtwayland             | False     |  [True, False]                         |
| qt3d                  | False     |  [True, False]                         |
| qtimageformats        | False     |  [True, False]                         |
| qtgraphicaleffects    | False     |  [True, False]                         |
| qtquickcontrols       | False     |  [True, False]                         |
| qtserialbus           | False     |  [True, False]                         |
| qtserialport          | False     |  [True, False]                         |
| qtx11extras           | False     |  [True, False]                         |
| qtmacextras           | False     |  [True, False]                         |
| qtwinextras           | False     |  [True, False]                         |
| qtandroidextras       | False     |  [True, False]                         |
| qtwebsockets          | False     |  [True, False]                         |
| qtwebchannel          | False     |  [True, False]                         |
| qtwebengine           | False     |  [True, False]                         |
| qtcanvas3d            | False     |  [True, False]                         |
| qtwebview             | False     |  [True, False]                         |
| qtquickcontrols2      | False     |  [True, False]                         |
| qtpurchasing          | False     |  [True, False]                         |
| qtcharts              | False     |  [True, False]                         |
| qtdatavis3d           | False     |  [True, False]                         |
| qtvirtualkeyboard     | False     |  [True, False]                         |
| qtgamepad             | False     |  [True, False]                         |
| qtscxml               | False     |  [True, False]                         |
| qtspeech              | False     |  [True, False]                         |
| qtnetworkauth         | False     |  [True, False]                         |
| qtremoteobjects       | False     |  [True, False]                         |
| qtwebglplugin         | False     |  [True, False]                         |
| qtlottie              | False     |  [True, False]                         |
| qtquicktimeline       | False     |  [True, False]                         |
| qtquick3d             | False     |  [True, False]                         |

## License Information

Bincrafters packages are hosted on [Bintray](https://bintray.com) and contain software which is licensed by the software's maintainers and NOT Bincrafters.

The contents of this GIT repository are completely separate from the software being packaged and therefore licensed separately. The license for all files contained in this GIT repository are defined in the [LICENSE.md](LICENSE.md) file in this repository. The licenses included with all Conan packages published by Bincrafters can be found in the Conan package directories in the following locations, relative to the Conan Cache root (`~/.conan` by default):

    ~/.conan/data/<pkg_name>/<pkg_version>/bincrafters/package/<random_package_id>/license/<LICENSE_FILES_HERE>

*Note :   The most common filenames for OSS licenses are `LICENSE` AND `COPYING` without file extensions.*
