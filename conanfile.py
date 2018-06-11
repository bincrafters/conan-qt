#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
from distutils.spawn import find_executable
from conans import VisualStudioBuildEnvironment
import os
import shutil

class QtConan(ConanFile):
    name = "Qt"
    version = "5.11.0"
    description = "Conan.io package for Qt library."
    url = "https://github.com/lucienboillod/conan-qt"
    license = "http://doc.qt.io/qt-5/lgpl.html"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    submodules = [
        "qt3d",
        "qtactiveqt",
        "qtandroidextras",
        "qtcanvas3d",
        "qtcharts",
        "qtconnectivity",
        "qtdatavis3d",
        "qtdeclarative",
        "qtdoc",
        "qtgamepad",
        "qtgraphicaleffects",
        "qtimageformats",
        "qtlocation",
        "qtmacextras",
        "qtmultimedia",
        "qtnetworkauth",
        "qtpurchasing",
        "qtquickcontrols",
        "qtquickcontrols2",
        "qtscript",
        "qtscxml",
        "qtsensors",
        "qtserialbus",
        "qtserialport",
        "qtspeech",
        "qtsvg",
        "qttools",
        "qttranslations",
        "qtvirtualkeyboard",
        "qtwayland",
        "qtwebchannel",
        "qtwebengine",
        "qtwebsockets",
        "qtwebview",
        "qtwinextras",
        "qtx11extras",
        "qtxmlpatterns"]
    options = dict({
        "shared": [True, False],
        "fPIC": [True, False],
        "opengl": ["desktop", "dynamic"],
        "openssl": ["no", "yes", "linked"],
        }, **{module[2:]: [True,False] for module in submodules}
    )
    no_copy_source = True
    default_options = ("shared=True", "fPIC=True", "opengl=desktop", "openssl=no") + tuple(module[2:] + "=False" for module in submodules)
    short_paths = True

    def build_requirements(self):
        if tools.os_info.is_linux:    
            pack_names = ["libfontconfig1-dev", "libxrender-dev",
                          "libxext-dev", "libxfixes-dev", "libxi-dev",
                          "libgl1-mesa-dev", "libxcb1-dev",
                          "libx11-xcb-dev",
                          "libxcb-keysyms1-dev", "libxcb-image0-dev",
                          "libxcb-shm0-dev", "libx11-dev",
                          "libxcb-icccm4-dev", "libxcb-sync-dev",
                          "libxcb-xfixes0-dev", "libxcb-shape0-dev", "libxcb-render-util0-dev",
                          "libxcb-randr0-dev", 
                          "libxcb-glx0-dev"]

            if self.settings.arch == "x86":
                pack_names = [item+":i386" for item in pack_names]

            installer = tools.SystemPackageTool()
            installer.update() # Update the package database
            installer.install(" ".join(pack_names)) # Install the package

    def config_options(self):
        if self.settings.os != "Windows":
            del self.options.opengl
            del self.options.openssl

    def requirements(self):
        if tools.os_info.is_windows:
            if self.options.openssl == "yes" or self.options.openssl == "linked":
                self.requires("OpenSSL/1.0.2l@conan/stable")
        
        if tools.os_info.is_linux:
            pack_names = ["libfontconfig1", "libxrender1",
                          "libxext6", "libxfixes3", "libxi6",
                          "libgl1-mesa-dri", "libxcb1",
                          "libx11-xcb1",
                          "libxcb-keysyms1", "libxcb-image0",
                          "libxcb-shm0", "libx11-6",
                          "libxcb-icccm4", "libxcb-sync1",
                          "libxcb-xfixes0", "libxcb-shape0", "libxcb-render-util0",
                          "libxcb-randr0", 
                          "libxcb-glx0"]

            if self.settings.arch == "x86":
                pack_names = [item+":i386" for item in pack_names]

            installer = tools.SystemPackageTool()
            installer.update() # Update the package database
            installer.install(" ".join(pack_names)) # Install the package

    def source(self):
        url = "http://download.qt.io/official_releases/qt/{0}/{1}/single/qt-everywhere-src-{1}"\
            .format(self.version[:self.version.rfind('.')], self.version)
        if tools.os_info.is_windows:
            tools.get("%s.zip" % url)
        else:
            self.run("wget -qO- %s.tar.xz | tar -xJ " % url)
        shutil.move("qt-everywhere-src-%s" % self.version, "qt5")

    def build(self):
        args = ["-opensource", "-confirm-license", "-nomake examples", "-nomake tests",
                "-prefix %s" % self.package_folder]
        if not self.options.shared:
            args.insert(0, "-static")
            if self.settings.os == "Windows":
                if self.settings.compiler.runtime == "MT":
                    args.append("-static-runtime")
        else:
            args.insert(0, "-shared")
        if self.settings.build_type == "Debug":
            args.append("-debug")
        else:
            args.append("-release")
        for module in self.submodules:
            if not getattr(self.options, module[2:]):
                args.append("-skip " + module)

        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                self._build_msvc(args)
            else:
                self._build_mingw(args)
        else:
            self._build_unix(args)

    def _build_msvc(self, args):
        build_command = find_executable("jom.exe")
        if build_command:
            build_args = ["-j", str(tools.cpu_count())]
        else:
            build_command = "nmake.exe"
            build_args = []
        self.output.info("Using '%s %s' to build" % (build_command, " ".join(build_args)))

        with tools.environment_append(VisualStudioBuildEnvironment(self).vars):
            vcvars = tools.vcvars_command(self.settings)

            args += ["-opengl %s" % self.options.opengl]
            if self.options.openssl == "no":
                args += ["-no-openssl"]
            elif self.options.openssl == "yes":
                args += ["-openssl"]
            else:
                args += ["-openssl-linked"]

            self.run("%s && set" % vcvars)
            self.run("%s && %s/qt5/configure %s"
                     % (vcvars, self.source_folder, " ".join(args)))
            self.run("%s && %s %s"
                     % (vcvars, build_command, " ".join(build_args)))
            self.run("%s && %s install" % (vcvars, build_command))

    def _build_mingw(self, args):
        # Workaround for configure using clang first if in the path
        new_path = []
        for item in os.environ['PATH'].split(';'):
            if item != 'C:\\Program Files\\LLVM\\bin':
                new_path.append(item)
        os.environ['PATH'] = ';'.join(new_path)
        # end workaround
        args += ["-opengl %s" % self.options.opengl,
                 "-platform win32-g++"]

        self.output.info("Using '%d' threads" % tools.cpu_count())
        self.run("%s/qt5/configure.bat %s" % (self.source_folder, " ".join(args)))
        self.run("mingw32-make -j %d" % tools.cpu_count())
        self.run("mingw32-make install")

    def _build_unix(self, args):
        if self.settings.os == "Linux":
            args += ["-silent", "-xcb"]
            if self.settings.arch == "x86":
                args += ["-platform linux-g++-32"]
        else:
            args += ["-silent", "-no-framework"]
            if self.settings.arch == "x86":
                args += ["-platform macx-clang-32"]

        self.output.info("Using '%d' threads" % tools.cpu_count())
        self.run("%s/qt5/configure %s" % (self.source_folder, " ".join(args)))
        self.run("make -j %d" % tools.cpu_count())
        self.run("make install")

    def package_info(self):
        if self.settings.os == "Windows":
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)

