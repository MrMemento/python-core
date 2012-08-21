# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#---------
# IMPORTS
#---------

# global
import Tkinter

#----------------------
# GUI CONFIG CONSTANTS
#----------------------

class GuiConfigConstants( object ):
    '''
    Static class for tkinter anchor constant replacing.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    COMMAND  = 'command'

    ACTIVE   = Tkinter.ACTIVE
    ENABLED  = Tkinter.NORMAL
    DISABLED = Tkinter.DISABLED

    STATE_REPLACEMENTS = {
        'enabled':  Tkinter.NORMAL,
        'disabled': Tkinter.DISABLED,
        'active':   Tkinter.ACTIVE,
    }

    ANCHOR_REPLACEMENTS = {
        'nw': Tkinter.NW,
        'n':  Tkinter.N,
        'ne': Tkinter.NE,
        'w':  Tkinter.W,
        'c':  Tkinter.CENTER,
        'e':  Tkinter.E,
        'sw': Tkinter.SW,
        's':  Tkinter.S,
        'se': Tkinter.SE,
    }

    FILL_REPLACEMENTS = {
        'x':    Tkinter.X,
        'y':    Tkinter.Y,
        'both': Tkinter.BOTH,
        'none': Tkinter.NONE,
    }

    RELIEF_REPLACEMENTS = {
        'f': Tkinter.FLAT,
        'r': Tkinter.RAISED,
        's': Tkinter.SUNKEN,
        'g': Tkinter.GROOVE,
        'r': Tkinter.RIDGE,
    }

    SIDE_REPLACEMENTS = {
        't': Tkinter.TOP,
        'l': Tkinter.LEFT,
        'r': Tkinter.RIGHT,
        'b': Tkinter.BOTTOM,
    }

    JUSTIFY_REPLACEMENTS = {
        'l': Tkinter.LEFT,
        'c': Tkinter.CENTER,
        'r': Tkinter.RIGHT,
    }

    SELECTMODE_REPLACEMENTS = {
        's': Tkinter.SINGLE,
        'b': Tkinter.BROWSE,
        'm': Tkinter.MULTIPLE,
        'e': Tkinter.EXTENDED,
    }

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
