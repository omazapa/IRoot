CFLAGS= -I. -shared -fPIC -Wl,-soname,libStdHandler.so

default:cython

cython:
	python setup.py build
clean:
	rm -rf *.so *~ *.pyc build PyStdIOHandler.cpp TStdIOHandler.cpp TStdIOHandler.c
