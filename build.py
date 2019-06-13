#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_default
import os

if __name__ == "__main__":

    builder = build_template_default.get_builder(build_policy="outdated")
    if "android_ndk_installer" in os.getenv("CONAN_BUILD_REQUIRES", ""):
        for it in builder.items:
            it.settings['os'] = 'Android'
            it.settings['compiler.libcxx'] = 'libc++'
            it.settings['os.api_level'] = '25'
    builder.run()
