# Copyright 2011 by Barnabás Bucsy
#
# This file is part of The Memento Framework.
#
# The Memento Framework is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# The Memento Framework is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with The Memento Framework. If not, see
# <http://www.gnu.org/licenses/>.

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
