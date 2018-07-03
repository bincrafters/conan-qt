#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
from distutils.spawn import find_executable
import os
import shutil
import configparser

class QtConan(ConanFile):

    def getsubmodules():
        config = configparser.ConfigParser()
        config.read('qtmodules.conf')
        res = {}
        assert config.sections()
        for s in config.sections():
            section = str(s)
            assert section.startswith("submodule ")
            assert section.count('"') == 2
            modulename = section[section.find('"') + 1 : section.rfind('"')]
            status = str(config.get(section, "status"))
            if status != "obsolete" and status != "ignore":
                res[modulename] = {"branch":str(config.get(section, "branch")), "status":status, "path":str(config.get(section, "path"))}
                if config.has_option(section, "depends"):
                    res[modulename]["depends"] = [str(i) for i in config.get(section, "depends").split()]
                else:
                    res[modulename]["depends"] = []
        return res
    submodules = getsubmodules()

    name = "Qt"
    version = "5.11.0"
    description = "Conan.io package for Qt library."
    url = "https://github.com/bincrafters/conan-qt"
    homepage = "https://www.qt.io/"
    license = "http://doc.qt.io/qt-5/lgpl.html"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md", "qtmodules.conf"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "arch", "compiler", "build_type"

    options = dict({
        "shared": [True, False],
        "fPIC": [True, False],
        "opengl": ["no", "es2", "desktop", "dynamic"],
        "openssl": ["no", "yes", "linked"],
        }, **{module: [True,False] for module in submodules}
    )
    no_copy_source = True
    default_options = ("shared=True", "fPIC=True", "opengl=no", "openssl=no") + tuple(module + "=False" for module in submodules)
    short_paths = True
    build_policy = "missing"

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

    def configure(self):
        if self.options.openssl == "yes":
            self.requires("OpenSSL/1.1.0g@conan/stable")
            self.options["OpenSSL"].no_zlib = True
            self.options["OpenSSL"].shared = True
        if self.options.openssl == "linked":
            self.requires("OpenSSL/1.1.0g@conan/stable")
            self.options["OpenSSL"].no_zlib = True
            self.options["OpenSSL"].shared = False

        assert QtConan.version == QtConan.submodules['qtbase']['branch']
        def enablemodule(self, module):
            setattr(self.options, module, True)
            for req in QtConan.submodules[module]["depends"]:
                enablemodule(self, req)
        self.options.qtbase = True
        for module in QtConan.submodules:
            if getattr(self.options, module):
                enablemodule(self, module)

    def requirements(self):
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
                if self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd":
                    args.append("-static-runtime")
        else:
            args.insert(0, "-shared")
        if self.settings.build_type == "Debug":
            args.append("-debug")
        else:
            args.append("-release")
        for module in QtConan.submodules:
            if not getattr(self.options, module) and os.path.isdir(os.path.join(self.source_folder, 'qt5', QtConan.submodules[module]['path'])):
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
        if self.options.openssl == "no":
            args += ["-no-openssl"]
        elif self.options.openssl == "yes":
            args += ["-openssl"]
        else:
            args += ["-openssl-linked"]
        if self.options.openssl != "no":
            args += ["-I %s" % i for i in self.deps_cpp_info["OpenSSL"].include_paths]
            libs = self.deps_cpp_info["OpenSSL"].libs
            lib_paths = self.deps_cpp_info["OpenSSL"].lib_paths
            args += ["OPENSSL_LIBS=\"%s %s\"" % (" ".join(["-L"+i for i in lib_paths]), " ".join(["-l"+i for i in libs]))]
        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                self._build_msvc(args)
            else:
                self._build_mingw(args)
        else:
            self._build_unix(args)
            
        with open('qtbase/bin/qt.conf', 'w') as f: 
            f.write('[Paths]\nPrefix = ..')

    def _build_msvc(self, args):
        build_command = find_executable("jom.exe")
        if build_command:
            build_args = ["-j", str(tools.cpu_count())]
        else:
            build_command = "nmake.exe"
            build_args = []
        self.output.info("Using '%s %s' to build" % (build_command, " ".join(build_args)))


        vcvars = tools.vcvars_command(self.settings)

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
        args += ["-platform win32-g++"]

        with tools.environment_append({"MAKEFLAGS":"-j %d" % tools.cpu_count()}):
            self.output.info("Using '%d' threads" % tools.cpu_count())
            self.run("%s/qt5/configure.bat %s" % (self.source_folder, " ".join(args)))
            self.run("mingw32-make")
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

        with tools.environment_append({"MAKEFLAGS":"-j %d" % tools.cpu_count()}):
            self.output.info("Using '%d' threads" % tools.cpu_count())
            self.run("%s/qt5/configure %s" % (self.source_folder, " ".join(args)))
            self.run("make")
            self.run("make install")

    def package(self):
        self.copy("bin/qt.conf", src="qtbase")

    def package_info(self):
        if self.settings.os == "Windows":
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
