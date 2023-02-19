#!/usr/bin/env python3
from pymake import CMake, ECMakeVersion, EProjectLanguage

cmake = CMake(min_version=ECMakeVersion.V3_25)
project = cmake.add_project("HelloWorld", EProjectLanguage.Cpp)

# Set up presets
base_preset = cmake.add_preset("base")
base_preset.set_build_dir("_build")
base_preset.set_install_dir("_out")
base_preset.set_generator("Ninja")

debug_preset = cmake.add_preset("debug")
debug_preset.inherit_from(base_preset)
debug_preset.set_variable("CMAKE_BUILD_TYPE", "Debug")
debug_preset.set_install_dir("_out/debug")

release_preset = cmake.add_preset("release")
release_preset.inherit_from(base_preset)
release_preset.set_variable("CMAKE_BUILD_TYPE", "Release")
release_preset.set_install_dir("_out/release")

cmake.set_default_presets(release_preset)

# Set up the target for the Hello World binary
exe_target = project.add_executable("HelloWorld")
exe_target.add_sources("source.cpp")
exe_target.install()

cmake.build()
