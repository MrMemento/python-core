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

# custom

#---------------
# GUI COMPONENT
#---------------

class GuiComponent( object ):
    '''
    Base decorator class for widgets used in GUI.
    '''

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    _GUI_CONTROLLER_KEY = 'gui_controller'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self, *args, **kvargs ):
        '''
        Constructor.
        Because this is a decorator class, we might receive additional args / kvargs not meant to be used in this class' constructor.
        '''

        self._controller = None
        if kvargs.has_key( GuiComponent._GUI_CONTROLLER_KEY ):
            self._controller = kvargs[ GuiComponent._GUI_CONTROLLER_KEY ]

    #----------------
    # PUBLIC METHODS
    #----------------

    def register_controller( self, controller ):
        '''
        Register controller associated with component.
        If controller already registered to component, raises RuntimeError.
        '''

        if self._controller is not None:
            raise RuntimeError( 'Controller already registered to component!' )

        self._controller = controller
