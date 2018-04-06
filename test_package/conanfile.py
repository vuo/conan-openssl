from conans import ConanFile
import platform

class OpenSSLTestConan(ConanFile):
    generators = 'qbs'

    requires = 'llvm/3.3-5@vuo/stable'

    def build(self):
        self.run('qbs -f "%s"' % self.source_folder)

    def imports(self):
        self.copy('*', src='bin', dst='bin')
        self.copy('*', src='lib', dst='lib')

    def test(self):
        self.run('qbs run -f "%s"' % self.source_folder)
