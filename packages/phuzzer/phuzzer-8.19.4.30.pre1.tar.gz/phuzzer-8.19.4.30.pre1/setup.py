import os
from distutils.core import setup

setup(
    name='phuzzer', version='8.19.4.30.pre1', description="Python wrapper for multiarch AFL",
    packages=['phuzzer', 'phuzzer.extensions'],
    install_requires=['angr', 'shellphish-qemu', 'shellphish-afl', 'tqdm']
)
