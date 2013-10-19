#-----------------------------------------------------------------------------
#  Copyright (C) 2013 Omar Zapata, The IPython and ROOT Development Teams.
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

"""
==========================
 ROOT magics for IPython
==========================

{ROOTMAGICS_DOC}

Usage
=====

``%%root``

{ROOT_DOC}
"""

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from __future__ import print_function

import sys

from IPython.core.magic import Magics, magics_class, line_cell_magic

import ROOT 

from PyStdIOHandler import PyStdIOHandler

#-----------------------------------------------------------------------------
# Main classes
#-----------------------------------------------------------------------------

@magics_class
class ROOTMagics(Magics):
    """A set of magics useful for interactive work with CERN's ROOT.
    """
    def __init__(self, shell):
        """
        Parameters
        ----------
        shell : IPython shell

        """
        super(ROOTMagics, self).__init__(shell)
        self.root = ROOT.gROOT
        self.io_handler=PyStdIOHandler()

    def flush_output(self):
        stdout=self.io_handler.GetStdout()
        stderr=self.io_handler.GetStderr()
        if(stdout != ""): print(stdout, file=sys.stdout)
        if(stderr != ""): print(stderr, file=sys.stderr)
        
    @line_cell_magic
    def root(self, line, cell=None):
        """
        Execute code in ROOT.
        """
        src = str(line if cell is None else cell)
        self.io_handler.Clear();
        self.io_handler.InitCapture()
        try:
           Ans=self.root.ProcessLineSync(src.replace('\n',''))
        except NotImplementedError, e:
           self.io_handler.EndCapture()
           print("Not Implemented Error:",e,file=sys.stderr)
           self.flush_output()
           return False
        except RuntimeError, e:
           self.io_handler.EndCapture()
           print("Runtime Error:",e,file=sys.stderr)
           self.flush_output()
           return False
        except SyntaxError, e:
           self.io_handler.EndCapture()
           print("Syntax Error:",e,file=sys.stderr)
           self.flush_output()
           return False	   
        self.io_handler.EndCapture()
        self.flush_output()
        return True
      

# Add to the global docstring the class information.
__doc__ = __doc__.format(
    ROOTMAGICS_DOC = ' '*8 + "Documentation for ROOT Magic Here",
    ROOT_DOC = ' '*8 + "Documentation for ROOT Magic Here Too",
    )


#-----------------------------------------------------------------------------
# IPython registration entry point.
#-----------------------------------------------------------------------------

def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(ROOTMagics)
