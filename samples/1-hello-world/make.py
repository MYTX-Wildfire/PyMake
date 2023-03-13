#!/usr/bin/env python3
import argparse
from pymake import PyMake, ECMakeBuildType, ECMakeGenerator, ECMakeVersion, \
    EProjectLanguage, EScope

# Figure out whether the build should use CMake 3.14 or 3.25
parser = argparse.ArgumentParser()
parser.add_argument(
    "--cmake",
    choices=["3.14", "3.25"],
    default="3.14",
    help="The version of CMake to use."
)
cli_args = parser.parse_known_args()[0]

if cli_args.cmake == "3.14":
    target_cmake_version = ECMakeVersion.V3_14
elif cli_args.cmake == "3.25":
    target_cmake_version = ECMakeVersion.V3_25
else:
    raise RuntimeError(f"Unknown/unsupported CMake version: {cli_args.cmake}.")

# Set up the PyMake project
pymake = PyMake.create_project(target_cmake_version)
project = pymake.create_project_scope(
    "HelloProject",
    EProjectLanguage.CPP
)

# Set up presets
base_preset = pymake.add_preset("base")
base_preset.generator = ECMakeGenerator.Ninja

debug_preset = pymake.add_preset("debug", base_presets=base_preset)
debug_preset.cmake_build_type = ECMakeBuildType.Debug
debug_preset.build_path = "_build/debug"
debug_preset.install_path = "_out/debug"

release_preset = pymake.add_preset("release", base_presets=base_preset)
release_preset.cmake_build_type = ECMakeBuildType.Release
release_preset.build_path = "_build/release"
release_preset.install_path = "_out/release"

pymake.set_default_presets(release_preset)

# Set up targets
target_set = project.create_target_set("HelloTargetSet")
exe_target = target_set.add_executable("HelloWorld")
exe_target.add_sources(EScope.PRIVATE, "source.cpp")
exe_target.install()

# Build the project
pymake.build()
