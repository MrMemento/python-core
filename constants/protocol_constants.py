# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

class ProtocolConstants( object ):
    '''
    Static class holding protocol regarding constants.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    PROTOCOL      = 'protocol'
    FILE_PROTOCOL = 'file'
    WEB_PROTOCOL  = 'web'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
