#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from distutils.spawn import find_executable
from conans import AutoToolsBuildEnvironment, ConanFile, tools, VisualStudioBuildEnvironment
import os


class QtConan(ConanFile):
    name = "Qt"
    version = "5.9.3"
    description = "Conan.io package for Qt library."
    url = "https://github.com/lucienboillod/conan-qt"

    license = "http://doc.qt.io/qt-5/lgpl.html"
    exports = ["LICENSE.md"]
    source_dir = "qt5"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "opengl": ["desktop", "dynamic"],
        "activeqt": [True, False],
        "canvas3d": [True, False],
        "connectivity": [True, False],
        "gamepad": [True, False],
        "graphicaleffects": [True, False],
        "imageformats": [True, False],
        "location": [True, False],
        "serialport": [True, False],
        "svg": [True, False],
        "tools": [True, False],
        "translations": [True, False],
        "webengine": [True, False],
        "websockets": [True, False],
        "xmlpatterns": [True, False],
        "openssl": ["no", "yes", "linked"]
    }
    default_options = "shared=True", "fPIC=True", "opengl=desktop", "activeqt=False", \
                      "canvas3d=False", "connectivity=False", "gamepad=False", \
                      "graphicaleffects=False", "imageformats=False", "location=False", \
                      "serialport=False", "svg=False", "tools=False", "translations=False", \
                      "webengine=False", "websockets=False", "xmlpatterns=False", "openssl=no"
    url = "http://github.com/ImpressiveDev/conan-qt"
    license = "http://doc.qt.io/qt-5/lgpl.html"
    short_paths = True

    def system_requirements(self):
        pack_names = None
        if tools.os_info.linux_distro == "ubuntu":
            pack_names = ["libgl1-mesa-dev", "libxcb1", "libxcb1-dev",
                          "libx11-xcb1", "libx11-xcb-dev", "libxcb-keysyms1",
                          "libxcb-keysyms1-dev", "libxcb-image0", "libxcb-image0-dev",
                          "libxcb-shm0", "libxcb-shm0-dev", "libxcb-icccm4",
                          "libxcb-icccm4-dev", "libxcb-sync1", "libxcb-sync-dev",
                          "libxcb-xfixes0-dev", "libxrender-dev", "libxcb-shape0-dev",
                          "libxcb-randr0-dev", "libxcb-render-util0", "libxcb-render-util0-dev",
                          "libxcb-glx0-dev", "libxcb-xinerama0", "libxcb-xinerama0-dev"]

            if self.settings.arch == "x86":
                full_pack_names = []
                for pack_name in pack_names:
                    full_pack_names += [pack_name + ":i386"]
                pack_names = full_pack_names

        if pack_names:
            installer = tools.SystemPackageTool()
            installer.update() # Update the package database
            installer.install(" ".join(pack_names)) # Install the package

    def config_options(self):
        if self.settings.os != "Windows":
            del self.options.opengl
            del self.options.openssl

    def requirements(self):
        if self.settings.os == "Windows":
            if self.options.openssl == "yes":
                self.requires("OpenSSL/1.0.2l@conan/stable")
            elif self.options.openssl == "linked":
                self.requires("OpenSSL/1.0.2l@conan/stable")

    def source(self):
        submodules = ["qtbase"]

        if self.options.activeqt:
            submodules.append("qtactiveqt")
        if self.options.canvas3d:
            submodules.append("qtcanvas3d")
        if self.options.connectivity:
            submodules.append("qtconnectivity")
        if self.options.gamepad:
            submodules.append("qtgamepad")
        if self.options.graphicaleffects:
            submodules.append("qtgraphicaleffects")
        if self.options.imageformats:
            submodules.append("qtimageformats")
        if self.options.location:
            submodules.append("qtlocation")
        if self.options.serialport:
            submodules.append("qtserialport")
        if self.options.svg:
            submodules.append("qtsvg")
        if self.options.tools:
            submodules.append("qttools")
        if self.options.translations:
            submodules.append("qttranslations")
        if self.options.webengine:
            submodules.append("qtwebengine")
        if self.options.websockets:
            submodules.append("qtwebsockets")
        if self.options.xmlpatterns:
            submodules.append("qtxmlpatterns")

        self.run("git clone https://code.qt.io/qt/qt5.git")
        self.run("cd %s && git checkout v%s" % (self.source_dir, self.version))
        self.run("cd %s && git submodule update --init %s" % (self.source_dir, " ".join(submodules)))

        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.source_dir)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        args = ["-opensource", "-confirm-license", "-nomake examples", "-nomake tests",
                "-prefix %s" % self.package_folder]
        if not self.options.shared:
            args.insert(0, "-static")
        if self.settings.build_type == "Debug":
            args.append("-debug")
        else:
            args.append("-release")

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

        env = {}
        env.update({'PATH': ['%s/qtbase/bin' % self.source_folder,
                             '%s/gnuwin32/bin' % self.source_folder,
                             '%s/qtrepotools/bin' % self.source_folder]})

        env_build = VisualStudioBuildEnvironment(self)
        env.update(env_build.vars)

        # Workaround for conan-io/conan#1408
        for name, value in list(env.items()):
            if not value:
                del env[name]
        with tools.environment_append(env):
            vcvars = tools.vcvars_command(self.settings)

            args += ["-opengl %s" % self.options.opengl]
            if self.options.openssl == "no":
                args += ["-no-openssl"]
            elif self.options.openssl == "yes":
                args += ["-openssl"]
            else:
                args += ["-openssl-linked"]

            self.run("cd %s && %s && set" % (self.source_dir, vcvars))
            self.run("cd %s && %s && configure %s"
                     % (self.source_dir, vcvars, " ".join(args)))
            self.run("cd %s && %s && %s %s"
                     % (self.source_dir, vcvars, build_command, " ".join(build_args)))
            self.run("cd %s && %s && %s install" % (self.source_dir, vcvars, build_command))

    def _build_mingw(self, args):
        env_build = AutoToolsBuildEnvironment(self)
        env = {'PATH': ['%s/bin' % self.source_folder,
                        '%s/qtbase/bin' % self.source_folder,
                        '%s/gnuwin32/bin' % self.source_folder,
                        '%s/qtrepotools/bin' % self.source_folder]}
        env.update(env_build.vars)
        with tools.environment_append(env):
            # Workaround for configure using clang first if in the path
            new_path = []
            for item in os.environ['PATH'].split(';'):
                if item != 'C:\\Program Files\\LLVM\\bin':
                    new_path.append(item)
            os.environ['PATH'] = ';'.join(new_path)
            # end workaround
            args += ["-opengl %s" % self.options.opengl,
                     "-platform win32-g++"]

            self.output.info("Using '%s' threads" % str(tools.cpu_count()))
            self.run("cd %s && configure.bat %s"
                     % (self.source_dir, " ".join(args)))
            self.run("cd %s && mingw32-make -j %s"
                     % (self.source_dir, str(tools.cpu_count())))
            self.run("cd %s && mingw32-make install" % (self.source_dir))

    def _build_unix(self, args):
        if self.settings.os == "Linux":
            args += ["-silent", "-xcb"]
            if self.settings.arch == "x86":
                args += ["-platform linux-g++-32"]
        else:
            args += ["-silent", "-no-framework"]
            if self.settings.arch == "x86":
                args += ["-platform macx-clang-32"]

        self.output.info("Using '%s' threads" % str(tools.cpu_count()))
        self.run("cd %s && ./configure %s" % (self.source_dir, " ".join(args)))
        self.run("cd %s && make -j %s" % (self.source_dir, str(tools.cpu_count())))
        self.run("cd %s && make install" % (self.source_dir))

    def package_info(self):
        libs = ['Concurrent', 'Core', 'DBus',
                'Gui', 'Network', 'OpenGL',
                'Sql', 'Test', 'Widgets', 'Xml']

        self.cpp_info.libs = []
        self.cpp_info.includedirs = ["include"]
        for lib in libs:
            if self.settings.os == "Windows" and self.settings.build_type == "Debug":
                suffix = "d"
            elif self.settings.os == "Macos" and self.settings.build_type == "Debug":
                suffix = "_debug"
            else:
                suffix = ""
            self.cpp_info.libs += ["Qt5%s%s" % (lib, suffix)]
            self.cpp_info.includedirs += ["include/Qt%s" % lib]

        if self.settings.os == "Windows":
            # Some missing shared libs inside QML and others, but for the test it works
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
