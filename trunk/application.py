# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#---------
# IMPORTS
#---------

# global
import platform

# custom
from core.constants.sys_constants import SysConstants as SC
from core.utils.auto_dict import AutoDict

#------------------
# META PROGRAMMING
#------------------

class ApplicationMetaClass( type ):
    '''
    Metaclass to be used for multiple inheritance.
    '''

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    __APPLICATION_CLASS_NAME = 'Application'
    __CONSTRUCTOR_NAME       = '__init__'
    __INIT_FUNCTON_NAME      = 'init'

    def __new__( metaclass, class_name, class_bases, class_fields ):
        '''
        Internal function for creating descendant classes.
        '''

        # first Application class must be created
        if class_name is not ApplicationMetaClass.__APPLICATION_CLASS_NAME and Application in class_bases:

            # ensure inheritance order, Application must be the first one
            if class_bases[ 0 ] is not Application:
                raise RuntimeError( '"Application" class MUST be first ascendant of class "%s"!' % class_name )

            # ensure that Application.__init__( ) function is not overridden
            if ApplicationMetaClass.__CONSTRUCTOR_NAME in class_fields:
                raise RuntimeError( '"Application" class\'s "__init__( )" function MUST NOT be overridden in class "%s"! Use entry point function "init( )" instead!' % class_name )

            # ensure that Application.init( ) function is overridden
            if not ApplicationMetaClass.__INIT_FUNCTON_NAME in class_fields:
                raise RuntimeError( '"Application" class\'s "init( )" function MUST be overridden in class "%s"!' % class_name )

        # create the new class
        NewClass = super( ApplicationMetaClass, metaclass ).__new__( metaclass, class_name, class_bases, class_fields )

        # return the new class
        return NewClass

#-------------
# APPLICATION
#-------------

class Application( object ):
    '''
    Base application skeleton to be extended on particular purposes.
    '''

    #-----------
    # METACLASS
    #-----------

    __metaclass__ = ApplicationMetaClass

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    # different operating system platform keys
    _PLATFORM_ASSOCIATIONS = {
        'windows':   SC.WINDOWS,
        'microsoft': SC.WINDOWS,
        'linux':     SC.UNIX,
        'unix':      SC.UNIX,
        'darwin':    SC.OSX,
        'osx':       SC.OSX
    }

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self, *args, **kwargs ):
        '''
        Constructor.
        '''

        # run through all ancestor's __init__( ) functions when descendant is multiply inherited
        for ParentClass in self.__class__.__mro__:
            if ParentClass is not self.__class__ and ParentClass is not Application:

                #print( 'Running __init__ of class "%s"' % str( ParentClass ) )

                try:
                    ParentClass.__init__( self, *args, **kwargs )
                except Exception, e0:
                    try:
                        ParentClass.__init__( self )
                    except Exception, e1:
                        print( e0, e1 )
                        pass

        self.system_data = AutoDict( )

        # determine operating system
        self.system_data.operating_system = SC.NOT_SUPPORTED
        operating_system                  = platform.system( ).lower( )
        for key in Application._PLATFORM_ASSOCIATIONS:
            if operating_system.find( key ) > -1:
                self.system_data.operating_system = Application._PLATFORM_ASSOCIATIONS[ key ]
                break
        del operating_system

        self.init( *args, **kwargs )

    #------
    # INIT
    #------

    def init( self, *args, **kwargs ):
        '''
        Entry point for descendants. Should be overridden, raises RuntimeError otherwise.
        '''

        raise RuntimeError( 'Function "init( )" must be overridden!' )
