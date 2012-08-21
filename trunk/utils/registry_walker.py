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

#---------
# IMPORTS
#---------

# global
import re

#-----------------
# REGISTRY WALKER
#-----------------

class RegistryWalkwer( object ):
    '''
    Class for walking the registry tree.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    SUBKEYS               = '__/*SUBKEYS*\__'
    HKEY_CLASSES_ROOT     = 'HKEY_CLASSES_ROOT',
    HKEY_CURRENT_USER     = 'HKEY_CURRENT_USER',
    HKEY_LOCAL_MACHINE    = 'HKEY_LOCAL_MACHINE',
    HKEY_USERS            = 'HKEY_USERS',
    HKEY_PERFORMANCE_DATA = 'HKEY_PERFORMANCE_DATA',
    HKEY_CURRENT_CONFIG   = 'HKEY_CURRENT_CONFIG',
    HKEY_DYN_DATA         = 'HKEY_DYN_DATA'

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    # WindowsError: [Errno 259] No more data is available
    _WINREG_ACCEPTED_ERRORS = ( 259, '259' )
    _WINREG_SEPARATOR       = '\\'
    _WINREG_HKEYS           = (
        HKEY_CLASSES_ROOT,
        HKEY_CURRENT_USER,
        HKEY_LOCAL_MACHINE,
        HKEY_USERS,
        HKEY_PERFORMANCE_DATA,
        HKEY_CURRENT_CONFIG,
        HKEY_DYN_DATA,
    )

    #-----------------------
    # PUBLIC STATIC METHODS
    #-----------------------

    @staticmethod
    def build_object( home, path, patterns = None ):
        '''
        Build Python object out of registry entries.
        If "patterns" is set, only matching values names will be listed.
        '''

        import _winreg

        #-------------------------------------
        # INTERNAL RECURSIVE FUNCTION - START
        #-------------------------------------

        def _recursive_registry_walker( home, path, patterns ):

            current_key = _winreg.OpenKey( home, path )
            to_return   = { }

            # enumerate all values in current key
            count  = 0
            values = { }

            try:

                while True:
                    val_name, val_data, val_type = _winreg.EnumValue( current_key, count )
                    if val_type is _winreg.REG_SZ or val_type is _winreg.REG_EXPAND_SZ:
                        val_data = val_data.encode( 'utf-8' )

                    if patterns is None:
                        values[ val_name ] = val_data
                    else:
                        for pattern in patterns:
                            if re.match( pattern, val_name, re.IGNORECASE ):
                                values[ val_name ] = val_data
                                break
                    count += 1

            except Exception, e:

                if e[ 0 ] not in RegistryWalkwer._WINREG_ACCEPTED_ERRORS:
                    raise e

            # enumerate all sub keys in current key
            count = 0
            keys  = { }
            key   = ''

            try:

                while True:
                    key          = _winreg.EnumKey( current_key, count )
                    keys[ key ]  = _recursive_registry_walker( home, path + key + RegistryWalkwer._WINREG_SEPARATOR, patterns )
                    count       += 1

            except Exception, e:

                if e[ 0 ] not in RegistryWalkwer._WINREG_ACCEPTED_ERRORS:
                    raise e

            if count is not 0:
                values[ RegistryWalkwer.SUBKEYS ] = keys

            del keys
            del key
            del count

            _winreg.CloseKey( current_key )

            return values

        #-----------------------------------
        # INTERNAL RECURSIVE FUNCTION - END
        #-----------------------------------

        if home in RegistryWalkwer._WINREG_HKEYS:
            home = {
                RegistryWalkwer.HKEY_CLASSES_ROOT:     _winreg.HKEY_CLASSES_ROOT,
                RegistryWalkwer.HKEY_CURRENT_USER:     _winreg.HKEY_CURRENT_USER,
                RegistryWalkwer.HKEY_LOCAL_MACHINE:    _winreg.HKEY_LOCAL_MACHINE,
                RegistryWalkwer.HKEY_USERS:            _winreg.HKEY_USERS,
                RegistryWalkwer.HKEY_PERFORMANCE_DATA: _winreg.HKEY_PERFORMANCE_DATA,
                RegistryWalkwer.HKEY_CURRENT_CONFIG:   _winreg.HKEY_CURRENT_CONFIG,
                RegistryWalkwer.HKEY_DYN_DATA:         _winreg.HKEY_DYN_DATA,
            }[ home ]

        return _recursive_registry_walker( home, path, patterns )

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise Exception( 'Tried to instantiate static class!' )


