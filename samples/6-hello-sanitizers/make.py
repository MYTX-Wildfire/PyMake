#!/usr/bin/env python3
import argparse
from pymake import PyMake, ECMakeBuildType, ECMakeGenerator, ECMakeVersion, \
    EProjectLanguage, ESanitizerFlags

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
    "HelloGTest",
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

test_preset = pymake.add_preset("test", base_presets=debug_preset)
test_preset.targets = "test"

pymake.set_default_presets(release_preset)

# Add GoogleTest as an imported target
gtest_target_set = project.create_target_set("gtest_target_set")
gtest_main_target_set = project.create_target_set("gtest_main_target_set")

gtest_target = gtest_target_set.add_external_static_library("gtest")
gtest_target.set_location("/usr/lib", "gtest")

gtest_main_target = gtest_main_target_set.add_external_static_library(
    "gtest_main"
)
gtest_main_target.set_location("/usr/lib", "gtest_main")

# Register sanitized versions of GoogleTest
gtest_asan_target = gtest_target_set.add_external_static_library(
    "gtest_asan",
    sanitizer_flags=ESanitizerFlags.ADDRESS
)
gtest_target.set_location("/usr/lib", "gtest")

gtest_asan_main_target = gtest_main_target_set.add_external_static_library(
    "gtest_asan_main",
    sanitizer_flags=ESanitizerFlags.ADDRESS
)
gtest_main_target.set_location("/usr/lib", "gtest_main")

# Configure the project
pymake.add_subdirectory("foo")
pymake.add_subdirectory("test")

# Build the project
pymake.build()
