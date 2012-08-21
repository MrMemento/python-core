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
