#Copyright (C) 2013,  Omar Andres Zapata Mesa 
from libcpp.string cimport string

cdef extern from "TStdIOHandler.h" namespace "ROOT":
    cdef cppclass TStdIOHandler:
        TStdIOHandler()
        void InitCapture()
        void EndCapture()
        string GetStdout()
        string GetStderr()
        void Clear()
 
cdef class PyStdIOHandler:
    cdef TStdIOHandler *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self):
        self.thisptr = new TStdIOHandler()
    def __dealloc__(self):
        del self.thisptr
    def InitCapture(self):
        self.thisptr.InitCapture()
    def EndCapture(self):
        self.thisptr.EndCapture()
    def GetStdout(self):
        return self.thisptr.GetStdout()
    def GetStderr(self):
        return self.thisptr.GetStderr()
    def Clear(self):    
        self.thisptr.Clear()