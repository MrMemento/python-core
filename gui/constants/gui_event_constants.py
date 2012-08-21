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

#---------------------------
# COMPONENT EVENT CONSTANTS
#---------------------------

class ComponentEventConstants( object ):
    '''
    Static class holding component regarding constants.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    UPDATE     = 'Configure'
    ACTIVATE   = 'Activate'
    DEACTIVATE = 'Deactivate'
    REDRAW     = 'Expose'
    DESTROY    = 'Destroy'
    FOCUS_IN   = 'FocusIn'
    FOCUS_OUT  = 'FocusOut'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )

#-----------------------
# MOUSE EVENT CONSTANTS
#-----------------------

class MouseEventConstants( object ):
    '''
    Static class holding mouse regarding constants.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    MOTION    = 'Motion'
    ENTER     = 'Enter'
    LEAVE     = 'Leave'
    PRESS     = 'ButtonPress'
    RELEASE   = 'ButtonRelease'
    DOUBLE    = 'Double'
    TRIPLE    = 'Triple'
    QUADRUPLE = 'Quadruple'
    WHEEL     = 'MouseWheel'

    LEFT_BUTTON   = 1
    MIDDLE_BUTTON = 2
    RIGHT_BUTTON  = 3
    FOURTH_BUTTON = 4
    FIFTH_BUTTON  = 5

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )

#--------------------------
# KEYBOARD EVENT CONSTANTS
#--------------------------

class KeyboardEventConstants( object ):
    '''
    Static class holding keyboard regarding constants.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------
    
    PRESS   = 'KeyPress'
    RELEASE = 'KeyRelease'

    LEFT  = '_L'
    RIGHT = '_R'

    SHIFT       = 'Shift'
    ALT         = 'Alt'
    CONTROL     = 'Control'
    COMMAND     = 'Command'
    OPTION      = 'Option'
    ENTER       = 'Return'
    ESCAPE      = 'Escape'
    LOCK        = 'Lock'
    EXTENDED    = 'Extended'
    BREAK       = 'Cancel'
    PAUSE       = 'Pause'
    CAPS_LOCK   = 'Caps_Lock'
    NUM_LOCK    = 'Num_Lock'
    SCROLL_LOCK = 'Scroll_Lock'
    PAGE_UP     = 'Prior'
    PAGE_DOWN   = 'Next'
    HOME        = 'Home'
    END         = 'End'
    PRINT       = 'Print'
    INSERT      = 'Insert'
    DELETE      = 'Delete'
    BACKSPACE   = 'BackSpace'
    TAB         = 'Tab'
    LEFT        = 'Left'
    UP          = 'Up'
    RIGHT       = 'Right'
    DOWN        = 'Down'
    SPACE       = 'space'
    SLASH       = 'slash'
    F1          = 'F1'
    F2          = 'F2'
    F3          = 'F3'
    F4          = 'F4'
    F5          = 'F5'
    F6          = 'F6'
    F7          = 'F7'
    F8          = 'F8'
    F9          = 'F9'
    F10         = 'F10'
    F11         = 'F11'
    F12         = 'F12'
    META        = 'Meta'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )

class BinaryEventConstants( object ):
    '''
    Static class holding tkinter event names.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    # event bit masks
    BIT_SHIFT     = 0x001
    BIT_CAPSLOCK  = 0x002
    BIT_CONTROL   = 0x004
    BIT_LEFT_ALT  = 0x008
    BIT_NUMLOCK   = 0x010
    BIT_RIGHT_ALT = 0x080
    BIT_MB_1      = 0x100
    BIT_MB_2      = 0x200
    BIT_MB_3      = 0x400

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
    
