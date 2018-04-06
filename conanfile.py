from conans import ConanFile, tools
import platform

class OpenSSLConan(ConanFile):
    name = 'openssl'

    source_version = '1.0.2o'
    package_version = '1'
    version = '%s-%s' % (source_version, package_version)

    build_requires = 'llvm/3.3-5@vuo/stable'
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://www.openssl.org/'
    license = 'https://www.openssl.org/source/license.html'
    description = 'A toolkit for the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols'
    source_dir = 'openssl-%s' % source_version

    def source(self):
        tools.get('https://www.openssl.org/source/openssl-%s.tar.gz' % self.source_version,
                  sha256='ec3f5c9714ba0fd45cb4e087301eb1336c317e0d20b575a125050470e8089e4d')

        self.run('mv %s/LICENSE %s/%s.txt' % (self.source_dir, self.source_dir, self.name))

    def build(self):
        with tools.chdir(self.source_dir):
            flags = '-O0'

            if platform.system() == 'Darwin':
                flags += ' -mmacosx-version-min=10.10'
                target = 'darwin64-x86_64-cc'
            elif platform.system() == 'Linux':
                flags += ' -fPIC'
                target = 'linux-x86_64'

            env_vars = {
                'CC'     : self.deps_cpp_info['llvm'].rootpath + '/bin/clang',
                'CXX'    : self.deps_cpp_info['llvm'].rootpath + '/bin/clang++',
            }
            with tools.environment_append(env_vars):
                self.run('./Configure --openssldir=/usr/local/etc/openssl no-zlib no-shared no-hw no-asm ' + target + ' ' + flags)
                self.run('make -j9 --quiet')

    def package(self):
        self.copy('*.h', src='%s/include' % self.source_dir, dst='include')
        self.copy('*.a', src=self.source_dir,                dst='lib')
        self.copy('openssl', src='%s/apps' % self.source_dir, dst='bin')

        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')

    def package_info(self):
        self.cpp_info.libs = ['crypto', 'ssl']
