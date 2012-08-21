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
from core.gui.components.auto_scrollbar import AutoScrollbar

#------------------
# SCROLLABLE FRAME
#------------------

class ScrollableFrame( Frame ):
    '''
    Class for creating scrollable user interface elements.
    '''

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self, master, *args, **kvargs ):
        '''
        Constructor.
        '''

        Frame.__init__( self, master, *args, **kvargs )

        self._widget = None

        self._bar_y = AutoScrollbar( self )
        self._bar_y.grid(
            row    = 0,
            column = 1,
            sticky = N + S
        )

        self._bar_x = AutoScrollbar( self,
            orient = HORIZONTAL
        )
        self._bar_x.grid(
            row    = 1,
            column = 0,
            sticky = E + W
        )

        self.grid_rowconfigure( 0,
            weight = 1
        )
        self.grid_columnconfigure( 0,
            weight = 1
        )

    #----------------
    # PUBLIC METHODS
    #----------------

    def attach_widget( self, widget ):
        '''
        Attach a scrollable widget to teh ScrollableFrame.
        '''

        if not self._widget is None:
            raise TclError( 'Widget already attached!' )

        self._widget = widget
        self._widget.grid(
            row    = 0,
            column = 0,
            sticky = N + S + E + W
        )
        self._widget.configure(
            xscrollcommand = self._bar_x.set,
            yscrollcommand = self._bar_y.set,
            border         = 0
        )

        self._bar_x.config(
            command = self._widget.xview
        )
        self._bar_y.config(
            command = self._widget.yview
        )

        self.update_idletasks( )
