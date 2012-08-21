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

#----------------
# GUI CONTROLLER
#----------------

class GuiController( ):
    '''
    Base class for controllerrs used in GUI.
    '''

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self, dispatcher, root, os, translator ):
        '''
        Constructor.
        "dispatcher": The "Dispatcher" instance that manages communication between "GuiController" instances.
        "root": The tk root instance.
        '''

        self.components = [ ]
        self.dispatcher = dispatcher
        self.root       = root
        self.os         = os
        self.translate  = translator

    #----------------
    # PUBLIC METHODS
    #----------------

    def register_component( self, component ):
        '''
        Register a component who will call functions on this controller.
        '''

        if component in self.components:
            raise RuntimeError( 'Component already registered to controller "%s"' % self.__class__.__name__ )

        self.components.append( component )
        component.register_controller( self )
