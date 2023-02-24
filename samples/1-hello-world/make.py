#!/usr/bin/env python3
import argparse
from pymake import CMake314, CMake325, ECMakeBuildType, ECMakeGenerator, \
    EProjectLanguage

# Figure out whether the build should use CMake 3.14 or 3.25
parser = argparse.ArgumentParser()
parser.add_argument(
    "--cmake-version",
    choices=["3.14", "3.25"],
    default="3.25",
    help="The version of CMake to use."
)
cli_args = parser.parse_known_args()[0]

# Set up the CMake project
if cli_args.cmake_version == "3.14":
    cmake = CMake314()
else:
    cmake = CMake325()
project = cmake.add_project("HelloWorld", EProjectLanguage.Cpp)

# Set up presets
base_preset = cmake.add_preset("base")
base_preset.binary_dir = "_build"
base_preset.install_dir = "_out"
base_preset.generator = ECMakeGenerator.Ninja

debug_preset = cmake.add_preset("debug")
debug_preset.inherit_from(base_preset)
debug_preset.cmake_build_type = ECMakeBuildType.Debug
debug_preset.install_dir = "_out/debug"

release_preset = cmake.add_preset("release")
release_preset.inherit_from(base_preset)
release_preset.cmake_build_type = ECMakeBuildType.Release
release_preset.install_dir = "_out/release"

cmake.set_default_presets(release_preset)

# Set up the target for the Hello World binary
exe_target = project.add_executable("HelloWorld")
exe_target.add_sources("source.cpp")
exe_target.install()

cmake.build()
