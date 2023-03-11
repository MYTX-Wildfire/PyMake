#!/usr/bin/env python3
import argparse
from pymake import PyMake, ECMakeVersion, EProjectLanguage

# Figure out whether the build should use CMake 3.14 or 3.25
parser = argparse.ArgumentParser()
parser.add_argument(
    "--cmake",
    choices=["3.14", "3.25"],
    default="3.25",
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
    "HelloWorld",
    EProjectLanguage.CPP
)
target_set = project.create_target_set("HelloWorld")
