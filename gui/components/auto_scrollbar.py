# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#---------
# IMPORTS
#---------

# global
from Tkinter import *

#----------------
# AUTO SCROLLBAR
#----------------

class AutoScrollbar(Scrollbar):
    '''
    A Scrollbar that hides itself if it's not needed.
    Only works if the grid geometry manager is used.
    '''

    def set( self, lo, hi ):

        if float( lo ) <= 0.0 and float( hi ) >= 1.0:
            self.grid_remove( )
        else:
            self.grid( )

        Scrollbar.set( self, lo, hi )

    def pack( self, **kvargs ):
        raise TclError( 'Cannot use pack with this widget!' )

    def place( self, **kvargs ):
        raise TclError( 'Cannot use place with this widget!' )