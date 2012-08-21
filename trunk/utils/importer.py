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
