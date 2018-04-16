#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan.packager import ConanMultiPackager

if __name__ == "__main__":

    # builder = ConanMultiPackager(visual_versions=["15"], archs=["x86_64"], build_types=["Debug"], username="lboillod", channel="testing")
    # builder.add_common_builds()
    # filtered_builds = []
    # for settings, options, env_vars, build_requires in builder.builds:
    #     if settings["compiler"] == "Visual Studio":
    #         if settings["compiler.runtime"] == "MT" or settings["compiler.runtime"] == "MTd":
    #             # Ignore MT runtime
    #             continue
    #     if settings["arch"] != "x86_64":
    #         continue

    #     filtered_builds.append([settings, options, env_vars, build_requires])

    # builder.builds = filtered_builds

    builder = ConanMultiPackager(username="lboillod")
    builder.add(settings={"arch": "x86_64", "build_type": "Release", "compiler": "Visual Studio", "compiler.version": 15, "compiler.runtime": "MD"},
                options={}, env_vars={}, build_requires={})
    builder.run()
