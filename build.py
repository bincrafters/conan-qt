#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform

from bincrafters import build_template_default

if __name__ == "__main__":

    builder = build_template_default.get_builder(build_policy="missing")

    if platform.system() == "Windows":
        for settings, options, env_vars, build_requires in builder.builds:
            if options["qt:shared"] is False:
                # disable icu on windows in static build. see QTBUG-77120.
                options["qt:with_icu"] = False
    builder.run()
