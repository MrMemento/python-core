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

# custom
from core.gui.constants.gui_event_constants import ComponentEventConstants as CEC

from core.gui.common.gui_event_generator import GuiEventGenerator as GEG

#---------------
# WRAPPED LABEL
#---------------

class WrappedLabel( Label ):
    '''
    Wordwrapped label tkinter class.
    '''
    
    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    _BORDER_WIDTH = 'bd'
    _PAD_X        = 'padx'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self, master, *args, **kvargs ):
        '''
        Constructor.
        '''

        Label.__init__( self, master, *args, **kvargs )
        self.bind(
            GEG.get_event_string( CEC.UPDATE ),
            self._update_wrap_width
        )

    #-----------------
    # PRIVATE METHODS
    #-----------------

    def _update_wrap_width( self, event ):
        '''
        Private function for updating wrapwidth of Label.
        '''

        pad = ( int( str( self.cget( WrappedLabel._BORDER_WIDTH ) ) ) + int( str( self.cget( WrappedLabel._PAD_X ) ) ) ) *2
        self.configure(
            wraplength = event.width - pad
        )
