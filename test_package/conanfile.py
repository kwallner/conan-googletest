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
    
<<<<<<< HEAD
=======
    def configure(self):
        if self.settings.compiler == "Visual Studio" and self.settings.compiler.runtime == "MT" and self.settings.build_type == "Debug":
            self.settings.compiler.runtime = "MTd"

>>>>>>> release/1.8.1
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
        assert os.path.exists(os.path.join(self.deps_cpp_info["googletest"].rootpath, "LICENSE"))
