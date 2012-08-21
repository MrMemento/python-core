# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#---------
# IMPORTS
#---------

# global

# custom
from core.constants.sys_constants import SysConstants as SC
from core.gui.constants.gui_cursor_constants import GuiCursorConstants as GCC

#---------------
# MOUSE MANAGER
#---------------

class MouseManager( object ):
    '''
    Static class for managing mouse.
    '''

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    _OS   = None
    _ROOT = None

    #-----------------------
    # PUBLIC STATIC METHODS
    #-----------------------

    @staticmethod
    def set_os( operating_system ):
        '''
        Setter method for operating system.
        '''

        MouseManager._OS = operating_system

    @staticmethod
    def set_root( root ):
        '''
        Setter method for operating system.
        '''

        MouseManager._ROOT = root

    @staticmethod
    def show_inherited_cursor( master = None ):
        '''
        Change the cursor to busy.
        '''

        MouseManager.show_cursor(
            GCC.INHERITED,
            master
        )

    @staticmethod
    def show_busy_cursor( master = None ):
        '''
        Change the cursor to busy.
        '''

        MouseManager.show_cursor(
            GCC.WATCH,
            master
        )

    @staticmethod
    def show_arrow_cursor( master = None ):
        '''
        Change the cursor to busy.
        '''

        MouseManager.show_cursor(
            GCC.ARROW,
            master
        )

    @staticmethod
    def show_hand_cursor( master = None ):
        '''
        Change the cursor to busy.
        '''

        MouseManager.show_cursor(
            GCC.HAND1,
            master
        )

    @staticmethod
    def show_cursor( cursor, master = None ):
        '''
        Changes mouse cursor to given one.
        '''

        if MouseManager._OS is not SC.WINDOWS and cursor in GCC.WIN_NATIVES:
            raise RuntimeError( 'Trying to bind Windows native cursor on "%s" platform!' % MouseManager._OS )
        elif MouseManager._OS is not SC.OSX and cursor in GCC.OSX_NATIVES:
            raise RuntimeError( 'Trying to bind OSX native cursor on "%s" platform!' % MouseManager._OS )

        master = MouseManager._check_master( master )
        master.configure(
            cursor = cursor
        )
        master.update_idletasks( )

    #------------------------
    # PRIVATE STATIC METHODS
    #------------------------

    @staticmethod
    def _check_master( master ):
        '''
        Private function to return presented or default master tk instance.
        '''

        if master is None:

            if MouseManager._ROOT is None:
                raise RuntimeError( 'No master tk instance presented, and there is no default!' )

            return MouseManager._ROOT

        return master

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )