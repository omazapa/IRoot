#Copyright (C) 2013,  Omar Andres Zapata Mesa 
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

setup(
  ext_modules=[Extension(
    name="PyStdIOHandler",
    sources=["PyStdIOHandler.pyx","TStdIOHandler.cxx"], 
    language="c++")],
    cmdclass = {'build_ext': build_ext})