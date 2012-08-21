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

#---------------
# RUNTIME CLASS
#---------------

class RuntimeClass( object ):
    '''
    Static class for creating new classes runtime.
    '''

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    _CLASS_NAME_PREFIX = 'runtime::'

    #-----------------------
    # PUBLIC STATIC METHODS
    #-----------------------

    @staticmethod
    def get_inherited_class( class_name, *ascendants, **methods ):
        '''
        Creates inherited class runtime.
        "class_name": Name of the newly created class. Will be prefixed with static "_CLASS_PREFIX"
        "ascendants": Ascendant classes to be used in multiple inheritance.
        "methods": Extra methods and values to be created/overridden in new class instances.
        '''

        Class = type(
            RuntimeClass._CLASS_NAME_PREFIX + class_name,
            ascendants,
            methods
        )
        Class.__runtime_mro__ = ascendants
        return Class

    @staticmethod
    def get_decorated_class( class_name, DecorateeClass, DecoratorClass ):
        '''
        Creates a new decorated class runtime that calls DecorateeClass' and DecoratorClass' "__init__( )" method aswell.
        "class_name": Name of the newly created class. Will be prefixed with static "_CLASS_PREFIX"
        "DecorateeClass": The class to be decorated.
        "DecoratorClass": The class to decorate with.
        '''

        def constructor( self, *args, **kvargs ):
            '''
            Function to be used as newly created class' constructor.
            '''

            for Ascendant in self.__class__.__runtime_mro__:
                try:
                    Ascendant.__init__( self, *args, **kvargs )
                except Exception, e0:                
                    print( 
                        '%s:: Could not run constructor of decoratee class "%s" with presented *args and **kvargs. Trying without them. (Error: %s)' %
                        ( self.__class__.__name__, Ascendant.__name__, str( e0 ) )
                    )
                    try:
                        Ascendant.__init__( self )
                    except Exception, e1:
                        print(
                            '%s:: Could not run constructor without presented *args and **kvargs of decoratee class "%s". Trying without them. (Error: %s)' %
                            ( self.__class__.__name__, Ascendant.__name__, str( e0 ) )
                        )

        return RuntimeClass.get_inherited_class(
            class_name,
             DecoratorClass, DecorateeClass,
            __init__ = constructor
        )

    @staticmethod
    def get_decorated_instance( class_name, DecorateeClass, DecoratorClass, *args, **kvargs ):
        '''
        Helper function for creating instances of decorated classes.
        See "get_decorated_class( )" method for more info.
        '''

        return RuntimeClass.get_decorated_class(
            class_name,
            DecoratorClass, DecorateeClass
        )( *args, **kvargs )

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
