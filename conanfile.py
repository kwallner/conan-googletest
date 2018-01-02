import os

from conans import ConanFile, tools, CMake
from conans.util import files

class GTestConan(ConanFile):
    name = "gtest"
    version = "1.8.0"
    #branch = "release-" + version
    branch = "master"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = ("shared=False", "fPIC=True")
    url = "http://github.com/kwallner/conan-gtest"
    license = 'BSD 3-clause "New" or "Revised" License'
    description = "Google's C++ test framework"

    def source(self):
        self.run("git clone git@github.com:google/googletest.git")
        self.run("cd googletest && git checkout %s" % self.branch)
        
    def build(self):
        cmake = CMake(self)
        if self.settings.compiler == "Visual Studio" and "MD" in str(self.settings.compiler.runtime):
            cmake.definitions["gtest_force_shared_crt"] = "ON"
        
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON" if self.options.fPIC or self.options.shared else "OFF"

        cmake.configure(source_dir="%s/googletest" % self.source_folder)
        cmake.build()
        cmake.install()
        
    def package(self):
        # Copy the license files
        self.copy("LICENSE", src="googletest", dst=".", keep_path=False)
        self.copy("README.md", src="googletest", dst=".", keep_path=False)

    def package_info(self):
        debug_postfix= "d" if self.settings.build_type == "Debug" else ""
        self.cpp_info.libs = [
            "gmock" + debug_postfix, 
            "gmock_main" + debug_postfix, 
            "gtest" + debug_postfix, 
            "gtest_main" + debug_postfix
            ]

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")

        if self.options.shared:
            self.cpp_info.defines.append("GTEST_LINKED_AS_SHARED_LIBRARY=1")

        if float(str(self.settings.compiler.version)) >= 15 and self.settings.compiler == "Visual Studio":
            self.cpp_info.defines.append("GTEST_LANG_CXX11=1")
