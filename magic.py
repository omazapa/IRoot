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
        
    @line_cell_magic
    def root(self, line, cell=None):
        """
        Execute code in ROOT, and pull some of the results back into the
        Python namespace.
        """
        src = str(line if cell is None else cell)
        IOHandler=PyStdIOHandler()
        IOHandler.InitCapture()
        code=src.splitlines()
        for cline in code:
           try:
	       self.root.ProcessLine(cline)
	   except:    
               IOHandler.EndCapture()
               print(IOHandler.GetStdout(), file=sys.stdout)
               print(IOHandler.GetStderr(), file=sys.stderr)
               return False
        IOHandler.EndCapture()
        print(IOHandler.GetStdout(), file=sys.stdout)
        print(IOHandler.GetStderr(), file=sys.stderr)
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
