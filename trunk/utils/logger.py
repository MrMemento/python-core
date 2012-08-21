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

#--------
# LOGGER
#--------

class Logger( object ):
    '''
    Static class for formating and piping logs.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    ENABLED    = True
    INDENT_KEY = '_indent_'

    # logging levels
    FATAL   = 3
    ERROR   = 2
    WARNING = 1
    INFO    = 0

    if not ENABLED:

        @staticmethod
        def set_output_method( output_method ):
            pass

        @staticmethod
        def set_output_format( output_format ):
            pass

        @staticmethod
        def set_level( level ):
            pass

        @staticmethod
        def title( string ):
            pass

        @staticmethod
        def log( *args, **kvargs ):
            pass

        @staticmethod
        def sub( *args, **kvargs ):
            pass

        @staticmethod
        def s_title( string ):
            pass

        @staticmethod
        def s_log( *args, **kvargs ):
            pass

        @staticmethod
        def s_sub( *args, **kvargs ):
            pass

    else:

        #--------------------------
        # PRIVATE STATIC VARIABLES
        #--------------------------

        _LOG_PREFIX        = ' -> '
        _SUB_PREFIX        = '  * '
        _NEW_LINE_PREFIX   = '  | '
        _EMPTY_LINE_PREFIX = '    '
        _OUTPUT_METHOD     = None
        _OUTPUT_FORMAT     = 'utf-8'
        _LOGGING_LEVEL     = INFO

        #----------------
        # STATIC SETTERS
        #----------------

        @staticmethod
        def set_output_method( output_method ):
            '''
            Stores the function which gets called with the formated log string as argument.
            '''

            Logger._OUTPUT_METHOD = output_method

        @staticmethod
        def set_output_format( output_format ):
            '''
            Stores the format to decode logged strings to.
            '''

            Logger._OUTPUT_FORMAT = output_format

        @staticmethod
        def set_level( level ):
            '''
            Stores the minimal level from where logs appear.
            Use provided constants!
            '''

            Logger._LOGGING_LEVEL = level

        #--------------------------
        # STATIC LOGGING FUNCTIONS
        #--------------------------

        @staticmethod
        def title( string, **kwargs ):
            '''
            Writes fancy title log. Does nothing with empty string.
            '''

            if Logger._OUTPUT_METHOD is not None and len( string ) > 0:
                Logger._OUTPUT_METHOD( Logger.s_title( string, **kwargs ) )

        @staticmethod
        def log( *args, **kvargs ):
            '''
            Writes a new (optionally multiline) log.
            '''

            args  = list( args )
            level = 0
            if isinstance( args[ 0 ], int ):
                level = args[ 0 ]
                del args[ 0 ]

            if Logger._OUTPUT_METHOD is not None and level >= Logger._LOGGING_LEVEL:
                Logger._OUTPUT_METHOD( Logger.s_log( *args, **kvargs ) )

        @staticmethod
        def sub( *args, **kvargs ):
            '''
            Writes a new (optionally multiline) sub log element.
            '''

            args  = list( args )
            level = 0
            if isinstance( args[ 0 ], int ):
                level = args[ 0 ]
                del args[ 0 ]

            if Logger._OUTPUT_METHOD is not None and level >= Logger._LOGGING_LEVEL:
                Logger._OUTPUT_METHOD( Logger.s_sub( *args, **kvargs ) )

        #------------------
        # STRING FUNCTIONS
        #------------------

        @staticmethod
        def s_title( string, **kwargs ):
            '''
            Returns fancy title log. Returns empty string when entering empty string.
            '''

            string = string.decode( Logger._OUTPUT_FORMAT )
            s      = ( len( string ) +2 ) * '-'
            s      = s + '\n ' + string + '\n' + s
            return s

        @staticmethod
        def s_log( *args, **kvargs ):
            '''
            Returns a new (optionally multiline) log.
            '''

            if len( args ) > 0:
                return Logger._format(
                    args, kvargs,
                    Logger._LOG_PREFIX
                )

            else:
                return ''

        @staticmethod
        def s_sub( *args, **kvargs ):
            '''
            Returns a new (optionally multiline) sub log element.
            '''

            if kvargs.has_key( Logger.INDENT_KEY ):
                kvargs[ Logger.INDENT_KEY ] += 1
            else:
                kvargs[ Logger.INDENT_KEY ] = 1

            return Logger._format(
                args, kvargs,
                Logger._SUB_PREFIX
            )

        #------------------------
        # PRIVATE STATIC METHODS
        #------------------------

        @staticmethod
        def _format( args, kvargs, pref ):
            '''
            Private function for formating incoming arguments.
            '''

            args = list( args )

            # indent
            indent = 1
            if kvargs.has_key( Logger.INDENT_KEY ) and isinstance( kvargs[ Logger.INDENT_KEY ], int ) and kvargs[ Logger.INDENT_KEY ] > 0:
                indent = kvargs[ Logger.INDENT_KEY ] +1
                del kvargs[ Logger.INDENT_KEY ]

            for index, arg in enumerate( args ):
                args[ index ] = str( arg )

            indent = ( indent -1 ) * Logger._NEW_LINE_PREFIX
            s      = indent + pref + '\n'.join( args )
            s      = s.replace( '\n', '\n' + indent + Logger._EMPTY_LINE_PREFIX )
            s      = s.decode( Logger._OUTPUT_FORMAT )
            return s

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor. Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )

#-------------
# LOGGER USER
#-------------

class LoggerUser( object ):
    '''
    Base proxy class for Logger using applications.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    # logging levels
    LOG_FATAL   = Logger.FATAL
    LOG_ERROR   = Logger.ERROR
    LOG_WARNING = Logger.WARNING
    LOG_INFO    = Logger.INFO

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Constructor.
        '''

        pass

    #----------------
    # PUBLIC METHODS
    #----------------

    def logger_set_output_method( self, output_method ):
        '''
        Stores the function which gets called with the formated log string as argument.
        '''

        Logger.set_output_method( output_method )

    def logger_set_output_format( self, output_format ):
        '''
        Stores the format to decode logged strings to.
        '''

        Logger.set_output_format( output_format )

    def logger_set_level( self, level ):
        '''
        Stores the minimal level from where logs appear.
        Use provided constants!
        '''

        Logger.set_level( level )

    def title( self, string, **kwargs ):
        '''
        Writes fancy title log. Does nothing with empty string.
        '''

        Logger.title( string, **kvargs )

    def log( self, *args, **kvargs ):
        '''
        Writes a new (optionally multiline) log.
        '''

        Logger.log( *args, **kvargs )

    def sub( self, *args, **kvargs ):
        '''
        Writes a new (optionally multiline) sub log element.
        '''

        Logger.sub( *args, **kvargs )
