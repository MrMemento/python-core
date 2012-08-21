# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#-----------------
# EVENT CONSTANTS
#-----------------

class EventConstants( object ):
    '''
    Static class holding event names.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    KILL             = 'kill'
    PANIC            = 'panic'
    ABOUT            = 'about'
    HELP             = 'help'
    FOUND            = 'found'
    NOT_FOUND        = 'not_found'
    SHOW_STATE       = 'show_state'
    STATE_SHOWN      = 'state_shown'
    STATE_HIDDEN     = 'state_hidden'
    UPDATE_STATUSBAR = 'update_statusbar'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
    
