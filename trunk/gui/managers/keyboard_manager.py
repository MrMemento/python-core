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

#------------------
# KEYBOARD MANAGER
#------------------

class KeyboardManager( object ):
    '''
    Static class for managing keyboard.
    '''

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    _OS   = None

    #-----------------------
    # PUBLIC STATIC METHODS
    #-----------------------

    @staticmethod
    def set_os( operating_system ):
        '''
        Setter method for operating system.
        '''

        KeyboardManager._OS = operating_system

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )