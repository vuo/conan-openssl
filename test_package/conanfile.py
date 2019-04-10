from conans import ConanFile, CMake
import platform

class OpenSSLTestConan(ConanFile):
    generators = 'cmake'

    requires = 'llvm/3.3-5@vuo/stable'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy('*', src='bin', dst='bin')
        self.copy('*', src='lib', dst='lib')

    def test(self):
        self.run('./bin/test_package')
