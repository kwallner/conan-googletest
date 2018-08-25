import os
from shutil import copyfile

from conans import ConanFile, tools, CMake
from conans.util import files

class GTestConan(ConanFile):
    name = "gtest"
    version = "1.8.0"
    scm = { "type": "git", "url": "https://github.com/google/googletest.git", "revision": "master" }
    #branch = "release-" + version
    branch = "master"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = ("shared=False", "fPIC=True")
    url = "http://github.com/kwallner/conan-gtest"
    license = 'BSD 3-clause "New" or "Revised" License'
    description = "Google's C++ test framework"

     
    def configure(self):
        if self.settings.compiler == "Visual Studio" and self.settings.compiler.runtime == "MT" and self.settings.build_type == "Debug":
            self.settings.compiler.runtime = "MTd"

    def config(self):
        # There seems to be a bug when using a shared version, see:
        # https://groups.google.com/forum/#!msg/googletestframework/LGVrYGnKlHM/UD6KnOhTJ08J
        if self.settings.os == "Linux":
            self.options.shared=False
    
    def source(self):
        # No debug postfix
        tools.replace_in_file("googletest/cmake/internal_utils.cmake",
            'DEBUG_POSTFIX "d"', 'DEBUG_POSTFIX ""')
        
    def build(self):
        cmake = CMake(self)
        if self.settings.compiler == "Visual Studio" and "MD" in str(self.settings.compiler.runtime):
            cmake.definitions["gtest_force_shared_crt"] = "ON"
        
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["GTEST_CREATE_SHARED_LIBRARY"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON" if self.options.fPIC or self.options.shared else "OFF"

        cmake.definitions["BUILD_GTEST"] = "ON" 
        cmake.definitions["BUILD_GMOCK"] = "ON"

        # No debug postfix
        cmake.definitions["CMAKE_DEBUG_POSTFIX"] = ""
        
        cmake.configure()
        cmake.build()
        cmake.install()
               
    def package(self):
        # Copy the license files
        self.copy("LICENSE", src="googletest", dst=".", keep_path=False)
        self.copy("README.md", src="googletest", dst=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [
            "gmock",
            "gmock_main", 
            "gtest", 
            "gtest_main"
            ]
            
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")

        if self.options.shared:
            self.cpp_info.defines.append("GTEST_LINKED_AS_SHARED_LIBRARY=1")

        if float(str(self.settings.compiler.version)) >= 15 and self.settings.compiler == "Visual Studio":
            self.cpp_info.defines.append("GTEST_LANG_CXX11=1")

        self.env_info.GTEST_ROOT = self.package_folder