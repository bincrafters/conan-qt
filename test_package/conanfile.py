#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os
import shutil

from conans import ConanFile, CMake, tools


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch", "os_build", "arch_build"
    generators = "qt"

    def build_requirements(self):
        if tools.os_info.is_windows and self.settings.compiler == "Visual Studio":
            self.build_requires("jom_installer/1.1.2@bincrafters/stable")

    def _build_with_qmake(self):
        tools.mkdir("qmake_folder")
        with tools.chdir("qmake_folder"):
            self.output.info("Building with qmake")

            def _qmakebuild():
                args = [self.source_folder]

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
                             
                self.run("qmake %s" % " ".join(args), run_environment=True)
                if tools.os_info.is_windows:
                    if self.settings.compiler == "Visual Studio":
                        self.run("jom", run_environment=True)
                    else:
                        self.run("mingw32-make", run_environment=True)
                else:
                    self.run("make", run_environment=True)

            if self.settings.compiler == "Visual Studio":
                with tools.vcvars(self.settings):
                    _qmakebuild()
            else:
                _qmakebuild()

    def _build_with_cmake(self):
        if not self.options["qt"].shared:
            self.output.info(
                "disabled cmake test with static Qt, because of https://bugreports.qt.io/browse/QTBUG-38913")
        else:
            self.output.info("Building with CMake")
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def build(self):
        self._build_with_qmake()
        self._build_with_cmake()

    def _test_with_qmake(self):
        self.output.info("Testing qmake")
        if tools.os_info.is_windows:
            bin_path = str(self.settings.build_type).lower()
        elif tools.os_info.is_linux:
            bin_path = "."
        else:
            bin_path = os.path.join("test_package.app", "Contents", "MacOS")
        bin_path = os.path.join("qmake_folder", bin_path)
        shutil.copy("qt.conf", bin_path)
        self.run(os.path.join(bin_path, "test_package"), run_environment=True)

    def _test_with_cmake(self):
        if not self.options["qt"].shared:
            self.output.info(
                "disabled cmake test with static Qt, because of https://bugreports.qt.io/browse/QTBUG-38913")
        else:
            self.output.info("Testing CMake")
            if self.settings.compiler == "Visual Studio":
                bin_path = str(self.settings.build_type)
            else:
                bin_path = self.build_folder
            self.run(os.path.join(bin_path, "test_package"), run_environment=True)

    def test(self):
        if (not tools.cross_building(self.settings)) or\
                (self.settings.os_build == self.settings.os and self.settings.arch_build == "x86_64" and self.settings.arch == "x86"):
            self._test_with_qmake()
            self._test_with_cmake()
