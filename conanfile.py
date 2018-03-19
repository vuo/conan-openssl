from conans import ConanFile, tools

class OpenSSLConan(ConanFile):
    name = 'openssl'

    source_version = '1.0.2n'
    package_version = '1'
    version = '%s-%s' % (source_version, package_version)

    requires = 'llvm/3.3-1@vuo/stable'
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://www.openssl.org/'
    license = 'https://www.openssl.org/source/license.html'
    description = 'A toolkit for the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols'
    source_dir = 'openssl-%s' % source_version

    def source(self):
        tools.get('https://www.openssl.org/source/openssl-%s.tar.gz' % self.source_version,
                  sha256='370babb75f278c39e0c50e8c4e7493bc0f18db6867478341a832a982fd15a8fe')

    def build(self):
        with tools.chdir(self.source_dir):
            env_vars = {
                'CC'     : self.deps_cpp_info['llvm'].rootpath + '/bin/clang',
                'CXX'    : self.deps_cpp_info['llvm'].rootpath + '/bin/clang++',
                'CFLAGS' : '-O0 -mmacosx-version-min=10.10',
                'LDFLAGS': '-mmacosx-version-min=10.10',
            }
            with tools.environment_append(env_vars):
                self.run('./Configure --openssldir=/usr/local/etc/openssl no-zlib no-shared no-hw no-asm darwin64-x86_64-cc')
                self.run('make -j9 --quiet')

    def package(self):
        self.copy('*.h', src='%s/include' % self.source_dir, dst='include')
        self.copy('*.a', src=self.source_dir,                dst='lib')
        self.copy('openssl', src='%s/apps' % self.source_dir, dst='bin')

    def package_info(self):
        self.cpp_info.libs = ['crypto', 'ssl']
