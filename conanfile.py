from conans import ConanFile, tools
import os
import platform

class OpenSSLConan(ConanFile):
    name = 'openssl'

    source_version = '1.1.1h'
    package_version = '0'
    version = '%s-%s' % (source_version, package_version)

    build_requires = (
        'llvm/5.0.2-1@vuo/stable',
        'macos-sdk/11.0-0@vuo/stable',
        # 'vuoutils/1.2@vuo/stable',
    )
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://www.openssl.org/'
    license = 'https://www.openssl.org/source/license.html'
    description = 'A toolkit for the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols'
    source_dir = 'openssl-%s' % source_version

    build_x86_dir = '_build_x86'
    build_arm_dir = '_build_arm'
    install_x86_dir = '_install_x86'
    install_arm_dir = '_install_arm'
    install_universal_dir = '_install_universal'

    exports_sources = '*.patch'

    def source(self):
        tools.get('https://www.openssl.org/source/openssl-%s.tar.gz' % self.source_version,
                  sha256='5c9ca8774bd7b03e5784f26ae9e9e6d749c9da2438545077e6b3d755a06595d9')

        # https://patch-diff.githubusercontent.com/raw/openssl/openssl/pull/12369
        tools.patch(patch_file='12369.patch', base_path=self.source_dir)

        self.run('mv %s/LICENSE %s/%s.txt' % (self.source_dir, self.source_dir, self.name))

    def build(self):
        flags = '-O0'
        flags += ' -mmacosx-version-min=10.11'
        flags += ' -isysroot%s' % self.deps_cpp_info['macos-sdk'].rootpath
        flags += ' no-deprecated'
        flags += ' no-zlib'
        flags += ' no-hw'
        flags += ' no-asm'

        # For US export compliance.
        flags += ' no-dso'
        flags += ' no-shared'

        env_vars = {
            'CC'     : self.deps_cpp_info['llvm'].rootpath + '/bin/clang',
            'CXX'    : self.deps_cpp_info['llvm'].rootpath + '/bin/clang++',
        }
        with tools.environment_append(env_vars):
            self.output.info("=== Build for x86_64 ===")
            tools.mkdir(self.build_x86_dir)
            with tools.chdir(self.build_x86_dir):
                target = 'darwin64-x86_64-cc'
                target += ' --prefix=%s/../%s' % (os.getcwd(), self.install_x86_dir)
                self.run('../%s/Configure --openssldir=/usr/local/etc/openssl %s %s' % (self.source_dir, target, flags))
                self.run('make -j9 --quiet')
                self.run('make install_sw --quiet')

            self.output.info("=== Build for arm64 ===")
            tools.mkdir(self.build_arm_dir)
            with tools.chdir(self.build_arm_dir):
                target = 'darwin64-arm64-cc'
                target += ' --prefix=%s/../%s' % (os.getcwd(), self.install_arm_dir)
                self.run('../%s/Configure --openssldir=/usr/local/etc/openssl %s %s' % (self.source_dir, target, flags))
                self.run('make -j9 --quiet')
                self.run('make install_sw --quiet')

    def package(self):
        tools.mkdir(self.install_universal_dir)
        with tools.chdir(self.install_universal_dir):
            self.run('lipo -create ../%s/lib/libcrypto.a ../%s/lib/libcrypto.a -output libcrypto.a' % (self.install_x86_dir, self.install_arm_dir))
            self.run('lipo -create ../%s/lib/libssl.a ../%s/lib/libssl.a -output libssl.a' % (self.install_x86_dir, self.install_arm_dir))
            self.run('lipo -create ../%s/bin/openssl ../%s/bin/openssl -output openssl' % (self.install_x86_dir, self.install_arm_dir))

        self.copy('*.h', src='%s/include' % self.install_x86_dir, dst='include')
        self.copy('*.a', src=self.install_universal_dir, dst='lib')
        self.copy('openssl', src=self.install_universal_dir, dst='bin')

        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')

    def package_info(self):
        self.cpp_info.libs = ['crypto', 'ssl']
