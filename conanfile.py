#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys

import configparser
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
from conans.model import Generator


class qt(Generator):
    @property
    def filename(self):
        return "qt.conf"

    @property
    def content(self):
        return "[Paths]\nPrefix = %s\n" % self.conanfile.deps_cpp_info["qt"].rootpath.replace("\\", "/")


class QtConan(ConanFile):

    def _getsubmodules():
        config = configparser.ConfigParser()
        config.read('qtmodules.conf')
        res = {}
        assert config.sections()
        for s in config.sections():
            section = str(s)
            assert section.startswith("submodule ")
            assert section.count('"') == 2
            modulename = section[section.find('"') + 1: section.rfind('"')]
            status = str(config.get(section, "status"))
            if status != "obsolete" and status != "ignore":
                res[modulename] = {"branch": str(config.get(section, "branch")), "status": status,
                                   "path": str(config.get(section, "path")), "depends": []}
                if config.has_option(section, "depends"):
                    res[modulename]["depends"] = [str(i) for i in config.get(section, "depends").split()]
        return res

    _submodules = _getsubmodules()

    name = "qt"
    version = "5.11.3"
    description = "Qt is a cross-platform framework for graphical user interfaces."
    topics = ("conan", "qt", "ui")
    url = "https://github.com/bincrafters/conan-qt"
    homepage = "https://www.qt.io"
    license = "LGPL-3.0-only"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md", "qtmodules.conf", "*.diff"]
    settings = "os", "arch", "compiler", "build_type"

    options = dict({
        "shared": [True, False],
        "commercial": [True, False],
        "opengl": ["no", "es2", "desktop", "dynamic"],
        "openssl": [True, False],
        "GUI": [True, False],
        "widgets": [True, False],
        "device": "ANY",
        "cross_compile": "ANY",
        "config": "ANY",
    }, **{module: [True, False] for module in _submodules if module != 'qtbase'}
    )
    no_copy_source = True
    default_options = dict({
        "shared": True,
        "commercial": False,
        "opengl": "desktop",
        "openssl": False,
        "GUI": True,
        "widgets": True,
        "device": None,
        "cross_compile": None,
        "config": None,
    }, **{module: False for module in _submodules if module != 'qtbase'}
    )
    short_paths = True

    def _system_package_architecture(self):
        if tools.os_info.with_apt:
            if self.settings.arch == "x86":
                return ':i386'
            elif self.settings.arch == "x86_64":
                return ':amd64'
            elif self.settings.arch == "armv6" or self.settings.arch == "armv7":
                return ':armel'
            elif self.settings.arch == "armv7hf":
                return ':armhf'
            elif self.settings.arch == "armv8":
                return ':arm64'

        if tools.os_info.with_yum:
            if self.settings.arch == "x86":
                return '.i686'
            elif self.settings.arch == 'x86_64':
                return '.x86_64'
        return ""

    def build_requirements(self):
        if self.options.GUI:
            pack_names = []
            if tools.os_info.with_apt:
                pack_names = ["libxcb1-dev", "libx11-dev", "libc6-dev"]
            elif tools.os_info.is_linux and not tools.os_info.with_pacman:
                pack_names = ["libxcb-devel", "libX11-devel", "glibc-devel"]

            if pack_names:
                installer = tools.SystemPackageTool()
                for item in pack_names:
                    installer.install(item + self._system_package_architecture())

        if tools.os_info.is_windows and self.settings.compiler == "Visual Studio":
            self.build_requires("jom_installer/1.1.2@bincrafters/stable")

    def configure(self):
        if self.options.openssl:
            self.requires("OpenSSL/1.1.0g@conan/stable")
            self.options["OpenSSL"].no_zlib = True
        if self.options.widgets:
            self.options.GUI = True
        if not self.options.GUI:
            self.options.opengl = "no"
        if self.settings.os == "Android" and self.options.opengl == "desktop":
            raise ConanInvalidConfiguration("OpenGL desktop is not supported on Android. Consider using OpenGL es2")

        assert QtConan.version == QtConan._submodules['qtbase']['branch']

        def _enablemodule(mod):
            if mod != 'qtbase':
                setattr(self.options, mod, True)
            for req in QtConan._submodules[mod]["depends"]:
                _enablemodule(req)

        for module in QtConan._submodules:
            if module != 'qtbase' and getattr(self.options, module):
                _enablemodule(module)

    def system_requirements(self):
        if self.options.GUI:
            pack_names = []
            if tools.os_info.is_linux:
                if tools.os_info.with_apt:
                    pack_names = ["libxcb1", "libx11-6"]
                    if self.options.opengl == "desktop":
                        pack_names.append("libgl1-mesa-dev")
                    elif self.options.opengl == "es2":
                        pack_names.append("libgles2-mesa-dev")
                else:
                    if not tools.os_info.linux_distro.startswith("opensuse"):
                        pack_names = ["libxcb"]
                    if not tools.os_info.with_pacman:
                        if self.options.opengl == "desktop":
                            if tools.os_info.linux_distro.startswith("opensuse"):
                                pack_names.append("Mesa-libGL-devel")
                            else:
                                pack_names.append("mesa-libGL-devel")

            if pack_names:
                installer = tools.SystemPackageTool()
                for item in pack_names:
                    installer.install(item + self._system_package_architecture())

    def source(self):
        url = "https://download.qt.io/official_releases/qt/{0}/{1}/single/qt-everywhere-src-{1}" \
            .format(self.version[:self.version.rfind('.')], self.version)
        if tools.os_info.is_windows:
            tools.get("%s.zip" % url, md5='9a57b251658d985c26acb6de18b69328')
        elif sys.version_info.major >= 3:
            tools.get("%s.tar.xz" % url, md5='02b353bfe7a40a8dc4274e1d17226d2b')
        else:  # python 2 cannot deal with .xz archives
            self.run("wget -qO- %s.tar.xz | tar -xJ " % url)
        shutil.move("qt-everywhere-src-%s" % self.version, "qt5")

        for patch in ["cc04651dea4c4678c626cb31b3ec8394426e2b25.diff"]:
            tools.patch("qt5/qtbase", patch)

    def _xplatform(self):
        if self.settings.os == "Linux":
            if self.settings.compiler == "gcc":
                return {"x86": "linux-g++-32",
                        "armv6": "linux-arm-gnueabi-g++",
                        "armv7": "linux-arm-gnueabi-g++",
                        "armv7hf": "linux-arm-gnueabi-g++",
                        "armv8": "linux-aarch64-gnu-g++"}.get(str(self.settings.arch), "linux-g++")
            elif self.settings.compiler == "clang":
                if self.settings.arch == "x86":
                    return "linux-clang-libc++-32" if self.settings.compiler.libcxx == "libc++" else "linux-clang-32"
                elif self.settings.arch == "x86_64":
                    return "linux-clang-libc++" if self.settings.compiler.libcxx == "libc++" else "linux-clang"

        elif self.settings.os == "Macos":
            return {"clang": "macx-clang",
                    "apple-clang": "macx-clang",
                    "gcc": "macx-g++"}.get(str(self.settings.compiler))

        elif self.settings.os == "iOS":
            if self.settings.compiler == "clang":
                return "macx-ios-clang"

        elif self.settings.os == "watchOS":
            if self.settings.compiler == "clang":
                return "macx-watchos-clang"

        elif self.settings.os == "tvOS":
            if self.settings.compiler == "clang":
                return "macx-tvos-clang"

        elif self.settings.os == "Android":
            return {"clang": "android-clang",
                    "gcc": "android-g++"}.get(str(self.settings.compiler))

        elif self.settings.os == "Windows":
            return {"Visual Studio": "win32-msvc",
                    "gcc": "win32-g++",
                    "clang": "win32-clang-g++"}.get(str(self.settings.compiler))

        elif self.settings.os == "WindowsStore":
            if self.settings.compiler == "Visual Studio":
                return {"14": {"armv7": "winrt-arm-msvc2015",
                               "x86": "winrt-x86-msvc2015",
                               "x86_64": "winrt-x64-msvc2015"},
                        "15": {"armv7": "winrt-arm-msvc2017",
                               "x86": "winrt-x86-msvc2017",
                               "x86_64": "winrt-x64-msvc2017"}
                        }.get(str(self.settings.compiler.version)).get(str(self.settings.arch))

        elif self.settings.os == "FreeBSD":
            return {"clang": "freebsd-clang",
                    "gcc": "freebsd-g++"}.get(str(self.settings.compiler))

        elif self.settings.os == "SunOS":
            if self.settings.compiler == "sun-cc":
                if self.settings.arch == "sparc":
                    return "solaris-cc-stlport" if self.settings.compiler.libcxx == "libstlport" else "solaris-cc"
                elif self.settings.arch == "sparcv9":
                    return "solaris-cc64-stlport" if self.settings.compiler.libcxx == "libstlport" else "solaris-cc64"
            elif self.settings.compiler == "gcc":
                return {"sparc": "solaris-g++",
                        "sparcv9": "solaris-g++-64"}.get(str(self.settings.arch))

        return None

    def build(self):
        args = ["-confirm-license", "-silent", "-nomake examples", "-nomake tests",
                "-prefix %s" % self.package_folder]
        if self.options.commercial:
            args.append("-commercial")
        else:
            args.append("-opensource")
        if not self.options.GUI:
            args.append("-no-gui")
        if not self.options.widgets:
            args.append("-no-widgets")
        if not self.options.shared:
            args.insert(0, "-static")
            if self.settings.compiler == "Visual Studio":
                if self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd":
                    args.append("-static-runtime")
        else:
            args.insert(0, "-shared")
        if self.settings.build_type == "Debug":
            args.append("-debug")
        elif self.settings.build_type == "Release":
            args.append("-release")
        elif self.settings.build_type == "RelWithDebInfo":
            args.append("-release")
            args.append("-force-debug-info")
        elif self.settings.build_type == "MinSizeRel":
            args.append("-release")
            args.append("-optimize-size")
            
        for module in QtConan._submodules:
            if module != 'qtbase' and not getattr(self.options, module) \
                    and os.path.isdir(os.path.join(self.source_folder, 'qt5', QtConan._submodules[module]['path'])):
                args.append("-skip " + module)

        # openGL
        if self.options.opengl == "no":
            args += ["-no-opengl"]
        elif self.options.opengl == "es2":
            args += ["-opengl es2"]
        elif self.options.opengl == "desktop":
            args += ["-opengl desktop"]
        if self.settings.os == "Windows":
            if self.options.opengl == "dynamic":
                args += ["-opengl dynamic"]

        # openSSL
        if not self.options.openssl:
            args += ["-no-openssl"]
        else:
            if self.options["OpenSSL"].shared:
                args += ["-openssl-linked"]
            else:
                args += ["-openssl"]
            args += ["-I %s" % i for i in self.deps_cpp_info["OpenSSL"].include_paths]
            libs = self.deps_cpp_info["OpenSSL"].libs
            lib_paths = self.deps_cpp_info["OpenSSL"].lib_paths
            os.environ["OPENSSL_LIBS"] = " ".join(["-L" + i for i in lib_paths] + ["-l" + i for i in libs])

        if self.settings.os == "Linux":
            if self.options.GUI:
                args.append("-qt-xcb")
        elif self.settings.os == "Macos":
            args += ["-no-framework"]
        elif self.settings.os == "Android":
            args += ["-android-ndk-platform android-%s" % self.settings.os.api_level]
            args += ["-android-arch %s" % {"armv6": "armeabi",
                                           "armv7": "armeabi-v7a",
                                           "armv8": "arm64-v8a",
                                           "x86": "x86",
                                           "x86_64": "x86_64",
                                           "mips": "mips",
                                           "mips64": "mips64"}.get(str(self.settings.arch))]
            # args += ["-android-toolchain-version %s" % self.settings.compiler.version]

        if self.options.device:
            args += ["-device %s" % self.options.device]
            if self.options.cross_compile:
                args += ["-device-option CROSS_COMPILE=%s" % self.options.cross_compile]
        else:
            xplatform_val = self._xplatform()
            if xplatform_val:
                args += ["-xplatform %s" % xplatform_val]
            else:
                self.output.warn("host not supported: %s %s %s %s" %
                                 (self.settings.os, self.settings.compiler,
                                  self.settings.compiler.version, self.settings.arch))

        def _getenvpath(var):
            val = os.getenv(var)
            if val and tools.os_info.is_windows:
                val = val.replace("\\", "/")
                os.environ[var] = val
            return val

        value = _getenvpath('CC')
        if value:
            args += ['QMAKE_CC=' + value,
                     'QMAKE_LINK_C=' + value,
                     'QMAKE_LINK_C_SHLIB=' + value]

        value = _getenvpath('CXX')
        if value:
            args += ['QMAKE_CXX=' + value,
                     'QMAKE_LINK=' + value,
                     'QMAKE_LINK_SHLIB=' + value]

        if self.options.config:
            args.append(str(self.options.config))

        args.append("-qt-zlib")

        def _build(make):
            with tools.environment_append({"MAKEFLAGS": "j%d" % tools.cpu_count()}):
                self.run("%s/qt5/configure %s" % (self.source_folder, " ".join(args)))
                self.run(make)
                self.run("%s install" % make)

        if tools.os_info.is_windows:
            if self.settings.compiler == "Visual Studio":
                with tools.vcvars(self.settings):
                    _build("jom")
            else:
                # Workaround for configure using clang first if in the path
                new_path = []
                for item in os.environ['PATH'].split(';'):
                    if item != 'C:\\Program Files\\LLVM\\bin':
                        new_path.append(item)
                os.environ['PATH'] = ';'.join(new_path)
                # end workaround
                _build("mingw32-make")
        else:
            _build("make")

        with open('qtbase/bin/qt.conf', 'w') as f:
            f.write('[Paths]\nPrefix = ..')

    def package(self):
        self.copy("bin/qt.conf", src="qtbase")

    def package_info(self):
        if self.settings.os == "Windows":
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
