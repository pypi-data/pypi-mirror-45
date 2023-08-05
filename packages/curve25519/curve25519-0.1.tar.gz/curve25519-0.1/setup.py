from __future__ import print_function
from glob import glob
from setuptools import setup,Extension

sources = ['curve25519module.c', 'curve/curve25519-donna.c']
sources.extend(glob("curve/ed25519/*.c"))
sources.extend(glob("curve/ed25519/additions/*.c"))
sources.extend(glob("curve/ed25519/nacl_sha512/*.c"))
#headers = ['curve25519-donna.h']
module_curve = Extension('curve25519',
                    sources = sorted(sources),
#                   headers = headers,
                    include_dirs = [
                      'curve/ed25519/nacl_includes',
                      'curve/ed25519/additions',
                      'curve/ed25519'
                      ]
                    )
setup(
    name='curve25519',
    version="0.1",
    license='GPLv3 License',
    ext_modules = [module_curve],
    description='curve25519 with ed25519 signatures, used by libaxolotl',
    platforms='any'
)
