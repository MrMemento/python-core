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