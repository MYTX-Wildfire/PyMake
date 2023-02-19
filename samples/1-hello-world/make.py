#!/usr/bin/env python3
from pymake import CMake, ECMakeVersion, EProjectLanguage

cmake = CMake(min_version=ECMakeVersion.V3_25)
project = cmake.add_project("HelloWorld", EProjectLanguage.Cpp)
exe_target = project.add_executable("HelloWorld")
exe_target.add_sources("source.cpp")
exe_target.install()

cmake.build()
