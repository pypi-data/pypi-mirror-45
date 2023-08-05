# -*- coding: utf-8 -*-
# imagecodecs_lite/setup.py

"""Imagecodecs_lite package setuptools script."""

import sys
import re

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

buildnumber = ''  # 'post0'

with open('imagecodecs/_imagecodecs_lite.pyx') as fh:
    code = fh.read()

version = re.search(r"__version__ = '(.*?)'", code).groups()[0]

version += ('.' + buildnumber) if buildnumber else ''

description = re.search(r'"""(.*)\.(?:\r\n|\r|\n)', code).groups()[0]

readme = re.search(r'(?:\r\n|\r|\n){2}"""(.*)"""(?:\r\n|\r|\n){2}__version__',
                   code, re.MULTILINE | re.DOTALL).groups()[0]

readme = '\n'.join([description, '=' * len(description)]
                   + readme.splitlines()[1:])

license = re.search(r'(# Copyright.*?(?:\r\n|\r|\n))(?:\r\n|\r|\n)+""', code,
                    re.MULTILINE | re.DOTALL).groups()[0]

license = license.replace('# ', '').replace('#', '')

if 'sdist' in sys.argv:
    with open('LICENSE', 'w') as fh:
        fh.write(license)
    with open('README.rst', 'w') as fh:
        fh.write(readme)


class build_ext(_build_ext):
    """Delay import numpy until build."""
    def finalize_options(self):
        _build_ext.finalize_options(self)
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


# Work around "Cython in setup_requires doesn't work"
# https://github.com/pypa/setuptools/issues/1317
try:
    import Cython  # noqa
    ext = '.pyx'
except ImportError:
    ext = '.c'

ext_modules = [
    Extension(
        'imagecodecs_lite._imagecodecs_lite',
        ['imagecodecs/imagecodecs.c', 'imagecodecs/_imagecodecs_lite' + ext],
        include_dirs=['imagecodecs'],
        libraries=[] if sys.platform == 'win32' else ['m'],
    )
]

setup_args = dict(
    name='imagecodecs-lite',
    version=version,
    description=description,
    long_description=readme,
    author='Christoph Gohlke',
    author_email='cgohlke@uci.edu',
    url='https://www.lfd.uci.edu/~gohlke/',
    python_requires='>=2.7',
    install_requires=['numpy>=1.11.3'],
    setup_requires=['setuptools>=18.0', 'numpy>=1.11.3'],  # , 'cython>=0.29.0'
    tests_require=['pytest'],
    packages=['imagecodecs_lite'],
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    license='BSD',
    zip_safe=False,
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    )

setup(**setup_args)
