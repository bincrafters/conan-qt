import os
import shutil
import itertools

import configparser
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
from conans.model import Generator
from conans.tools import Version


class qt(Generator):
    @property
    def filename(self):
        return "qt.conf"

    @property
    def content(self):
        return "[Paths]\nPrefix = %s\n" % self.conanfile.deps_cpp_info["qt"].rootpath.replace("\\", "/")


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


class QtConan(ConanFile):

    _submodules = _getsubmodules()

    generators = "pkg_config"
    name = "qt"
    description = "Qt is a cross-platform framework for graphical user interfaces."
    topics = ("conan", "qt", "ui")
    url = "https://github.com/bincrafters/conan-qt"
    homepage = "https://www.qt.io"
    license = "LGPL-3.0"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["qtmodules.conf", "patches/*.diff"]
    settings = "os", "arch", "compiler", "build_type"

    options = dict({
        "shared": [True, False],
        "commercial": [True, False],

        "opengl": ["no", "es2", "desktop", "dynamic"],
        "openssl": [True, False],
        "with_pcre2": [True, False],
        "with_glib": [True, False],
        # "with_libiconv": [True, False],  # Qt tests failure "invalid conversion from const char** to char**"
        "with_doubleconversion": [True, False],
        "with_freetype": [True, False],
        "with_fontconfig": [True, False],
        "with_icu": [True, False],
        "with_harfbuzz": [True, False],
        "with_libjpeg": [True, False],
        "with_libpng": [True, False],
        "with_sqlite3": [True, False],
        "with_mysql": [True, False],
        "with_pq": [True, False],
        "with_odbc": [True, False],
        "with_sdl2": [True, False],
        "with_libalsa": [True, False],
        "with_openal": [True, False],

        "GUI": [True, False],
        "widgets": [True, False],

        "device": "ANY",
        "cross_compile": "ANY",
        "sysroot": "ANY",
        "config": "ANY",
        "multiconfiguration": [True, False],
    }, **{module: [True, False] for module in _submodules if module != 'qtbase'}
    )
    no_copy_source = True
    default_options = dict({
        "shared": True,
        "commercial": False,
        "opengl": "desktop",
        "openssl": True,
        "with_pcre2": True,
        "with_glib": True,
        # "with_libiconv": True,
        "with_doubleconversion": True,
        "with_freetype": True,
        "with_fontconfig": True,
        "with_icu": True,
        "with_harfbuzz": True,
        "with_libjpeg": True,
        "with_libpng": True,
        "with_sqlite3": True,
        "with_mysql": True,
        "with_pq": True,
        "with_odbc": True,
        "with_sdl2": True,
        "with_libalsa": False,
        "with_openal": True,

        "GUI": True,
        "widgets": True,

        "device": None,
        "cross_compile": "/usr/bin/",
        "sysroot": None,
        "config": None,
        "multiconfiguration": False,
    }, **{module: False for module in _submodules if module != 'qtbase'}
    )
    requires = "zlib/1.2.11"
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
        if tools.os_info.is_windows and self.settings.compiler == "Visual Studio":
            self.build_requires("jom_installer/1.1.2@bincrafters/stable")
        if self.settings.os == 'Linux':
            if not tools.which('pkg-config'):
                self.build_requires('pkg-config_installer/0.29.2@bincrafters/stable')

    def config_options(self):
        if self.settings.os != "Linux":
            self.options.with_icu = False

    def configure(self):
        if self.settings.os != 'Linux':
            self.options.with_glib = False
        #     self.options.with_libiconv = False
            self.options.with_fontconfig = False
        if self.settings.compiler == "gcc" and Version(self.settings.compiler.version.value) < "5.3":
            self.options.with_mysql = False
        if self.settings.os == "Windows":
            self.options.with_mysql = False
            if not self.options.shared and self.options.with_icu:
                raise ConanInvalidConfiguration("icu option is not supported on windows in static build. see QTBUG-77120.")

        if self.options.widgets and not self.options.GUI:
            raise ConanInvalidConfiguration("using option qt:widgets without option qt:GUI is not possible. "
                                            "You can either disable qt:widgets or enable qt:GUI")
        if not self.options.GUI:
            self.options.opengl = "no"
            self.options.with_freetype = False
            self.options.with_fontconfig = False
            self.options.with_harfbuzz = False
            self.options.with_libjpeg = False
            self.options.with_libpng = False

        if not self.options.qtgamepad:
            self.options.with_sdl2 = False

        if not self.options.qtmultimedia:
            self.options.with_libalsa = False
            self.options.with_openal = False

        if self.settings.os != "Linux":
            self.options.with_libalsa = False

        if self.settings.os == "Android" and self.options.opengl == "desktop":
            raise ConanInvalidConfiguration("OpenGL desktop is not supported on Android. Consider using OpenGL es2")

        if self.settings.os != "Windows" and self.options.opengl == "dynamic":
            raise ConanInvalidConfiguration("Dynamic OpenGL is supported only on Windows.")

        if self.options.with_fontconfig and not self.options.with_freetype:
            raise ConanInvalidConfiguration("with_fontconfig cannot be enabled if with_freetype is disabled.")

        if self.settings.os == "Macos":
            del self.settings.os.version

        if self.options.multiconfiguration:
            del self.settings.build_type

        if not self.options.with_doubleconversion and str(self.settings.compiler.libcxx) != "libc++":
            raise ConanInvalidConfiguration('Qt without libc++ needs qt:with_doubleconversion. '
                                            'Either enable qt:with_doubleconversion or switch to libc++')

        assert self.version == self._submodules['qtbase']['branch']

        def _enablemodule(mod):
            if mod != 'qtbase':
                setattr(self.options, mod, True)
            for req in self._submodules[mod]["depends"]:
                _enablemodule(req)

        for module in self._submodules:
            if module != 'qtbase' and getattr(self.options, module):
                _enablemodule(module)

    def requirements(self):
        if self.options.openssl:
            self.requires("openssl/1.1.1d")
        if self.options.with_pcre2:
            self.requires("pcre2/10.33")

        if self.options.with_glib:
            self.requires("glib/2.58.3@bincrafters/stable")
        # if self.options.with_libiconv:
        #     self.requires("libiconv/1.15")
        if self.options.with_doubleconversion and not self.options.multiconfiguration:
            self.requires("double-conversion/3.1.5")
        if self.options.with_freetype and not self.options.multiconfiguration:
            self.requires("freetype/2.10.0")
        if self.options.with_fontconfig:
            self.requires("fontconfig/2.13.91@conan/stable")
        if self.options.with_icu:
            self.requires("icu/64.2")
        if self.options.with_harfbuzz and not self.options.multiconfiguration:
            self.requires("harfbuzz/2.6.2@bincrafters/stable")
        if self.options.with_libjpeg and not self.options.multiconfiguration:
            self.requires("libjpeg/9c")
        if self.options.with_libpng and not self.options.multiconfiguration:
            self.requires("libpng/1.6.37")
        if self.options.with_sqlite3 and not self.options.multiconfiguration:
            self.requires("sqlite3/3.29.0")
            self.options["sqlite3"].enable_column_metadata = True
        if self.options.with_mysql:
            self.requires("libmysqlclient/8.0.17")
        if self.options.with_pq:
            self.requires("libpq/11.5")
        if self.options.with_odbc:
            if self.settings.os != "Windows":
                self.requires("odbc/2.3.7")
        if self.options.with_sdl2:
            self.requires("sdl2/2.0.9@bincrafters/stable")
        if self.options.with_openal:
            self.requires("openal/1.19.0@bincrafters/stable")
        if self.options.with_libalsa:
            self.requires("libalsa/1.1.9")
        if self.options.GUI:
            if self.settings.os == "Linux" and not tools.cross_building(self.settings, skip_x64_x86=True):
                self.requires("xkbcommon/0.8.4@bincrafters/stable")

    def system_requirements(self):
        if self.options.GUI:
            pack_names = []
            if tools.os_info.is_linux:
                if tools.os_info.with_apt:
                    pack_names = ["libxcb1-dev", "libx11-dev", "libc6-dev"]
                    if self.options.opengl == "desktop":
                        pack_names.append("libgl1-mesa-dev")
                    elif self.options.opengl == "es2":
                        pack_names.append("libgles2-mesa-dev")
                else:
                    if not tools.os_info.linux_distro.startswith(("opensuse", "sles")):
                        pack_names = ["libxcb"]
                    if not tools.os_info.with_pacman:
                        pack_names += ["libxcb-devel", "libX11-devel", "glibc-devel"]
                        if self.options.opengl == "desktop":
                            if tools.os_info.linux_distro.startswith(("opensuse", "sles")):
                                pack_names.append("Mesa-libGL-devel")
                            else:
                                pack_names.append("mesa-libGL-devel")

            if pack_names:
                installer = tools.SystemPackageTool()
                for item in pack_names:
                    installer.install(item + self._system_package_architecture())

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        shutil.move("qt-everywhere-src-%s" % self.version, "qt5")

        for p in self.conan_data["patches"][self.version]:
            tools.patch(**p)

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
            if self.settings.compiler == "apple-clang":
                return "macx-ios-clang"

        elif self.settings.os == "watchOS":
            if self.settings.compiler == "apple-clang":
                return "macx-watchos-clang"

        elif self.settings.os == "tvOS":
            if self.settings.compiler == "apple-clang":
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
        elif self.settings.os == "Neutrino" and self.settings.compiler == "qcc":
            return {"armv8": "qnx-aarch64le-qcc",
                    "armv8.3": "qnx-aarch64le-qcc",
                    "armv7": "qnx-armle-v7-qcc",
                    "armv7hf": "qnx-armle-v7-qcc",
                    "armv7s": "qnx-armle-v7-qcc",
                    "armv7k": "qnx-armle-v7-qcc",
                    "x86": "qnx-x86-qcc",
                    "x86_64": "qnx-x86-64-qcc"}.get(str(self.settings.arch))

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
        if self.options.multiconfiguration:
            args.append("-debug-and-release")
        elif self.settings.build_type == "Debug":
            args.append("-debug")
        elif self.settings.build_type == "Release":
            args.append("-release")
        elif self.settings.build_type == "RelWithDebInfo":
            args.append("-release")
            args.append("-force-debug-info")
        elif self.settings.build_type == "MinSizeRel":
            args.append("-release")
            args.append("-optimize-size")

        for module in self._submodules:
            if module != 'qtbase' and not getattr(self.options, module) \
                    and os.path.isdir(os.path.join(self.source_folder, 'qt5', self._submodules[module]['path'])):
                args.append("-skip " + module)

        args.append("--zlib=system")

        # openGL
        if self.options.opengl == "no":
            args += ["-no-opengl"]
        elif self.options.opengl == "es2":
            args += ["-opengl es2"]
        elif self.options.opengl == "desktop":
            args += ["-opengl desktop"]
        elif self.options.opengl == "dynamic":
            args += ["-opengl dynamic"]

        # openSSL
        if not self.options.openssl:
            args += ["-no-openssl"]
        else:
            if self.options["openssl"].shared:
                args += ["-openssl-runtime"]
            else:
                args += ["-openssl-linked"]

        # args.append("--iconv=" + ("gnu" if self.options.with_libiconv else "no"))

        args.append("--glib=" + ("yes" if self.options.with_glib else "no"))
        args.append("--pcre=" + ("system" if self.options.with_pcre2 else "qt"))
        args.append("--fontconfig=" + ("yes" if self.options.with_fontconfig else "no"))
        args.append("--icu=" + ("yes" if self.options.with_icu else "no"))
        args.append("--sql-mysql=" + ("yes" if self.options.with_mysql else "no"))
        args.append("--sql-psql=" + ("yes" if self.options.with_pq else "no"))
        args.append("--sql-odbc=" + ("yes" if self.options.with_odbc else "no"))

        if self.options.qtmultimedia:
            args.append("--alsa=" + ("yes" if self.options.with_libalsa else "no"))

        for opt, conf_arg in [
                              ("with_doubleconversion", "doubleconversion"),
                              ("with_freetype", "freetype"),
                              ("with_harfbuzz", "harfbuzz"),
                              ("with_libjpeg", "libjpeg"),
                              ("with_libpng", "libpng"),
                              ("with_sqlite3", "sqlite")]:
            if getattr(self.options, opt):
                if self.options.multiconfiguration:
                    args += ["-qt-" + conf_arg]
                else:
                    args += ["-system-" + conf_arg]
            else:
                args += ["-no-" + conf_arg]

        libmap = [("zlib", "ZLIB"),
                  ("openssl", "OPENSSL"),
                  ("pcre2", "PCRE2"),
                  ("glib", "GLIB"),
                  # ("libiconv", "ICONV"),
                  ("double-conversion", "DOUBLECONVERSION"),
                  ("freetype", "FREETYPE"),
                  ("fontconfig", "FONTCONFIG"),
                  ("icu", "ICU"),
                  ("harfbuzz", "HARFBUZZ"),
                  ("libjpeg", "LIBJPEG"),
                  ("libpng", "LIBPNG"),
                  ("sqlite3", "SQLITE"),
                  ("libmysqlclient", "MYSQL"),
                  ("libpq", "PSQL"),
                  ("odbc", "ODBC"),
                  ("sdl2", "SDL2"),
                  ("openal", "OPENAL"),
                  ("libalsa", "ALSA")]
        libPaths = []
        for package, var in libmap:
            if package in self.deps_cpp_info.deps:
                if package == 'freetype':
                    args.append("\"%s_INCDIR=%s\"" % (var, self.deps_cpp_info[package].include_paths[-1]))
                else:
                    args += ["-I " + s for s in self.deps_cpp_info[package].include_paths]
                args += ["-D " + s for s in self.deps_cpp_info[package].defines]

                def _remove_duplicate(l):
                    seen = set()
                    seen_add = seen.add
                    for element in itertools.filterfalse(seen.__contains__, l):
                        seen_add(element)
                        yield element

                def _gather_libs(p):
                    libs = ["-l" + i for i in self.deps_cpp_info[p].libs]
                    if self.settings.os in ["Macos", "iOS", "watchOS", "tvOS"]:
                        libs += ["-framework " + i for i in self.deps_cpp_info[p].frameworks]
                    libs += self.deps_cpp_info[p].sharedlinkflags
                    for dep in self.deps_cpp_info[p].public_deps:
                        libs += _gather_libs(dep)
                    return _remove_duplicate(libs)
                args.append("\"%s_LIBS=%s\"" % (var, " ".join(_gather_libs(package))))

                def _gather_lib_paths(p):
                    lib_paths = self.deps_cpp_info[p].lib_paths
                    for dep in self.deps_cpp_info[p].public_deps:
                        lib_paths += _gather_lib_paths(dep)
                    return _remove_duplicate(lib_paths)
                libPaths += _gather_lib_paths(package)
        args += ["-L " + s for s in _remove_duplicate(libPaths)]

        if 'libmysqlclient' in self.deps_cpp_info.deps:
            args.append("-mysql_config " + os.path.join(self.deps_cpp_info['libmysqlclient'].rootpath, "bin", "mysql_config"))
        if 'libpq' in self.deps_cpp_info.deps:
            args.append("-psql_config " + os.path.join(self.deps_cpp_info['libpq'].rootpath, "bin", "pg_config"))
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

        if self.options.sysroot:
            args += ["-sysroot %s" % self.options.sysroot]

        if self.options.device:
            args += ["-device %s" % self.options.device]
            if self.options.cross_compile:
                args += ["-device-option CROSS_COMPILE=%s" % self.options.cross_compile]
        else:
            xplatform_val = self._xplatform()
            if xplatform_val:
                if not tools.cross_building(self.settings, skip_x64_x86=True):
                    args += ["-platform %s" % xplatform_val]
                else:
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
            args += ['QMAKE_CC="' + value + '"',
                     'QMAKE_LINK_C="' + value + '"',
                     'QMAKE_LINK_C_SHLIB="' + value + '"']

        value = _getenvpath('CXX')
        if value:
            args += ['QMAKE_CXX="' + value + '"',
                     'QMAKE_LINK="' + value + '"',
                     'QMAKE_LINK_SHLIB="' + value + '"']

        if tools.os_info.is_linux and self.settings.compiler == "clang":
            args += ['QMAKE_CXXFLAGS+="-ftemplate-depth=1024"']

        if self.options.config:
            args.append(str(self.options.config))

        for package in ['xkbcommon', 'glib']:
            if package in self.deps_cpp_info.deps:
                lib_path = self.deps_cpp_info[package].rootpath
                for dirpath, _, filenames in os.walk(lib_path):
                    for filename in filenames:
                        if filename.endswith('.pc'):
                            shutil.copyfile(os.path.join(dirpath, filename), filename)
                            tools.replace_prefix_in_pc_file(filename, lib_path)

        if 'glib' in self.deps_cpp_info.deps:
            shutil.move("pcre.pc", "libpcre.pc")
        with tools.vcvars(self.settings) if self.settings.compiler == "Visual Studio" else tools.no_op():
            with tools.environment_append({"MAKEFLAGS": "j%d" % tools.cpu_count(), "PKG_CONFIG_PATH": os.getcwd()}):
                try:
                    self.run("%s/qt5/configure %s" % (self.source_folder, " ".join(args)))
                finally:
                    self.output.info(open('config.log', errors='backslashreplace').read())

                if self.settings.compiler == "Visual Studio":
                    make = "jom"
                elif tools.os_info.is_windows:
                    make = "mingw32-make"
                else:
                    make = "make"
                self.run(make, run_environment=True)
                self.run("%s install" % make)

        with open('qtbase/bin/qt.conf', 'w') as f:
            f.write('[Paths]\nPrefix = ..')

    def package(self):
        self.copy("bin/qt.conf", src="qtbase")

    def package_id(self):
        # Backwards compatibility for cross_compile to not affect package_id
        # for people who don't use the `device` option
        self.info.options.cross_compile = None
        del self.info.options.sysroot


    def package_info(self):
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
