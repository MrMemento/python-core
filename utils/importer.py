#!/usr/bin/python
# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#----------
# IMPORTER
#----------

class Importer( object ):
    '''
    Static class for importing other classes runtime.
    '''

    #-----------------------
    # PUBLIC STATIC METHODS
    #-----------------------

    @staticmethod
    def import_by_path( class_path ):
        '''
        Imports a class based on "class_path" string.
        Returns imported class.
        '''

        module_name, class_name = class_path.rsplit( '.', 1 )
        return getattr( __import__( module_name, globals( ), locals( ), [ class_name ], -1 ), class_name )

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
