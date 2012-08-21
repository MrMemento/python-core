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

#----------------
# WINDOW MANAGER
#----------------

class WindowManager( object ):
    '''
    Static class for managing windows.
    '''

    #-----------------------
    # PUBLIC STATIC METHODS
    #-----------------------

    #

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )