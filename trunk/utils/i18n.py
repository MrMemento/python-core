# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#---------
# IMPORTS
#---------

# global
import urllib2
import json

# custom
from core.constants.protocol_constants import ProtocolConstants as PC
from core.utils.logger import Logger
from core.utils.auto_dict import AutoDict
from core.utils.script_formater import ScriptFormater

#------
# I18N
#------

class I18N( object ):
    '''
    Static class for handling translations.
    '''

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    _LOADED        = False
    _DICTIONARY    = { }
    _OUTPUT_FORMAT = 'utf-8'

    #-----------------------
    # PUBLIC STATIC METHODS
    #-----------------------

    @staticmethod
    def set_output_format( output_format ):
        '''
        Stores the format to decode strings to.
        '''

        I18N._OUTPUT_FORMAT = output_format

    @staticmethod
    def load_dictionary( dictionary_or_path, **kvargs ):
        '''
        Loads dictionary from path or URL.
        Default behaviour is loading from URL, can be overridden with kvarg "protocol".
        Use presented static constants in "ProtocolConstants".
        '''

        if isinstance( dictionary_or_path, dict ):

            I18N._DICTIONARY = dictionary_or_path

        elif isinstance( dictionary_or_path, str ):

            if kvargs.has_key( PC.PROTOCOL ) and kvargs[ PC.PROTOCOL ] == PC.FILE_PROTOCOL:
                data_source = open( dictionary_or_path )
            else:
                data_source = urllib2.urlopen( urllib2.Request( url = dictionary_or_path ) )

            json_data = data_source.read( )
            data_source.close( )

            # format json string, this way there may be comments in it for developers
            # be sure, to first remove comments, than new lines!
            json_data = ScriptFormater.remove_comments( json_data )
            json_data = ScriptFormater.remove_empty_lines( json_data )
            #print( json_data )

            I18N._DICTIONARY = json.loads( json_data )

        else:

            raise RuntimeError( '"I18N::load_dictionary( )" accepts only dictionary or path/url string! presented type is %s' % type( dictionary_or_path ) )

        I18N._LOADED = True

    @staticmethod
    def get( key, default_value = '' ):
        '''
        Get a deictionary entry for specified key. If it does not exist in dictionary, default value will be returned.
        '''

        if not I18N._LOADED:
            Logger.log( 1, 'I18N: Requesting translation before dictionary is loaded for key "%s"' % key )

        if I18N._DICTIONARY.has_key( key ):
            return I18N._DICTIONARY[ key ]

        else:
            if I18N._LOADED:
                Logger.log( 1, 'I18N: Dictionary entry for key "%s" was not found, using default value.' % key )
            return default_value

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )

#-----------
# I18N USER
#-----------

class I18NUser( object ):
    '''
    Base proxy class for internationalized applications.
    '''

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Constructor.
        '''

        pass

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    # do not use AutoDict, this way exceptions will warn programmer
    # to use all default keys
    DEFAULT_DICTIONARY = { }

    #----------------
    # PUBLIC METHODS
    #----------------

    def i18n_load_dictionary( self, dictionary_path, **kvargs ):
        '''
        Helper function for loading I18N dictionary.
        Loads dictionary from path or URL. Default behaviour is loading from URL, can be overridden with kvarg "protocol".
        Use presented static constants "I18N_FILE_PROTOCOL" or "I18N_WEB_PROTOCOL"
        '''

        I18N.load_dictionary( dictionary_path, **kvargs )

    def i18n_set_output_format( self, output_format ):
        '''
        Stores the format to decode strings to.
        '''

        I18N.set_output_format( output_format )

    def i18n( self, key ):
        '''
        Helper function for translation.
        Looks up key in loaded I18N dictionary, and uses default values from ascendent class' static "DEFAULT_DICTIONARY".
        '''

        return I18N.get( key, self.__class__.DEFAULT_DICTIONARY[ key ] )
