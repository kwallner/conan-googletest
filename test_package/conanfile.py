from conans.model.conan_file import ConanFile
from conans import CMake
import os


class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')
        
    def test(self):
        os.chdir("bin")
        self.run(".%smytest" % os.sep)
        assert os.path.exists(os.path.join(self.deps_cpp_info["gtest"].rootpath, "LICENSE"))
