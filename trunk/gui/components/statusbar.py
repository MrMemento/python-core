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

#-----------
# STATUSBAR
#-----------

class StatusBar( Frame ):
    '''
    Simple tkinter statusbar class.
    '''

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self, master, *args, **kvargs ):
        '''
        Constructor.
        '''

        Frame.__init__( self, master, *args, **kvargs )

        self.label = Label(
            self,
            borderwidth = 1,
            relief      = SUNKEN,
            anchor      = W
        )
        self.label.pack(
            fill = X
        )

    #----------------
    # PUBLIC METHODS
    #----------------

    def set_bar_text( self, label_text, *args ):
        '''
        Set statusbar text.
        '''

        self.label.config(
            text = label_text % args
        )
        self.label.update_idletasks( )

    def clear_bar_text( self ):
        '''
        Clear statusbar text.
        '''

        self.label.config(
            text = ''
        )
        self.label.update_idletasks( )

    def pack( self, *args, **kvargs ):
        '''
        Pack statusbar with side BOTTOM and fill X.
        '''

        kvargs[ 'side' ] = BOTTOM
        kvargs[ 'fill' ] = X

        return Frame.pack( self, *args, **kvargs )
