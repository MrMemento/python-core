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

#-----------------
# EVENT CONSTANTS
#-----------------

class EventConstants( object ):
    '''
    Static class holding event names.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    KILL             = 'kill'
    PANIC            = 'panic'
    ABOUT            = 'about'
    HELP             = 'help'
    FOUND            = 'found'
    NOT_FOUND        = 'not_found'
    SHOW_STATE       = 'show_state'
    STATE_SHOWN      = 'state_shown'
    STATE_HIDDEN     = 'state_hidden'
    UPDATE_STATUSBAR = 'update_statusbar'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
    
