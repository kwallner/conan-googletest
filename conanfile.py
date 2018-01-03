import os
from shutil import copyfile

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

    def config(self):
        # There seems to be a bug when using a shared version, see:
        # https://groups.google.com/forum/#!msg/googletestframework/LGVrYGnKlHM/UD6KnOhTJ08J
        if self.settings.os == "Linux":
            self.options.shared=False
    
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

        if self.settings.build_type == "Debug":
            # Hack to make FindGTest work: Find only works if release binaries are present
            if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
                copyfile("%s/lib/gmockd.lib" % self.package_folder, "%s/lib/gmock.lib" % self.package_folder)
                copyfile("%s/lib/gmock_maind.lib" % self.package_folder, "%s/lib/gmock_main.lib" % self.package_folder)
                copyfile("%s/lib/gtestd.lib" % self.package_folder, "%s/lib/gtest.lib" % self.package_folder)
                copyfile("%s/lib/gtest_maind.lib" % self.package_folder, "%s/lib/gtest_main.lib" % self.package_folder)
                if self.options.shared:
                    copyfile("%s/bin/gmockd.dll" % self.package_folder, "%s/bin/gmock.dll" % self.package_folder)
                    copyfile("%s/bin/gmock_maind.dll" % self.package_folder, "%s/bin/gmock_main.dll" % self.package_folder)
                    copyfile("%s/bin/gtestd.dll" % self.package_folder, "%s/bin/gtest.dll" % self.package_folder)
                    copyfile("%s/bin/gtest_maind.dll" % self.package_folder, "%s/bin/gtest_main.dll" % self.package_folder)
        
    def package_info(self):
        debug_postfix= "d" if self.settings.build_type == "Debug" else ""
        
        # Workround: No debug postfix here
        if self.settings.os == "Linux" and self.branch == "release-1.8.0":
            debug_postfix = ""
                
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
