# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#---------------
# SYS CONSTANTS
#---------------

class SysConstants( object ):
    '''
    Static class holding system regarding constants.
    '''

    # different operating system names
    WINDOWS       = 'Windows'
    UNIX          = 'Unix'
    OSX           = 'OSX'
    JAVA          = 'Java'
    NOT_SUPPORTED = 'Not Supported'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
