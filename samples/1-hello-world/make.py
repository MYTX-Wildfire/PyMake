#!/usr/bin/env python3
from pymake import CMake, ECMakeVersion

cmake = CMake(min_version=ECMakeVersion.V3_25)
cmake.build()
