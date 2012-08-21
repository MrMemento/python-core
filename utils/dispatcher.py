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

#------------
# DISPATCHER
#------------

class Dispatcher( object ):
    '''
    Basic event dispatcher class.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    STOP_PROPAGATION_IMMEDIATELY = 0
    STOP_PROPAGATION_PRIORITY    = 1

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Constructor.
        '''

        self._listeners = { }
        self._counter   = 0

    #------------------
    # PUBLIC FUNCTIONS
    #------------------

    def add_listener( self, event_name, callback_method, priority = 0 ):
        '''
        Subscribe for an event.
        '''

        if not isinstance( event_name, str ):
            raise RuntimeError( 'Parameter "event_name" must be type str, received type: "%s"' % type( event_name ) )
        elif not hasattr( callback_method, '__call__' ):
            raise RuntimeError( 'Parameter "callback_method" must be a (lambda) function, received type: "%s"' % type( callback_method ) )
        elif not isinstance( priority, int ):
            raise RuntimeError( 'Parameter "priority" must be type int, received type: "%s"' % type( priority ) )
        elif priority < 0:
            raise RuntimeError( 'Parameter "priority" MUST NOT be negative!' )

        if not event_name in self._listeners:
            self._listeners[ event_name ] = [ ( callback_method, priority, self._counter ) ]
        else:
            for i, t in enumerate( self._listeners[ event_name ] ):
                if t[ 0 ] is callback_method:
                    del self._listeners[ event_name ][ i ]
                    break
            self._listeners[ event_name ].append( ( callback_method, priority, self._counter ) )

        self._counter += 1

        self._listeners[ event_name ] = sorted( self._listeners[ event_name ],
            # sort by priority, then added
            key     = lambda listener_tuple: ( listener_tuple[ 1 ], listener_tuple[ 2 ] *-1 ),
            reverse = True
        )

    def remove_listener( self, event_name, callback_method ):
        '''
        Unsubscribe from an event.
        '''

        if not isinstance( event_name, str ):
            raise RuntimeError( 'Parameter "event_name" must be type str, received type: "%s"' % type( event_name ) )
        elif not hasattr( callback_method, '__call__' ):
            raise RuntimeError( 'Parameter "callback_method" must be a (lambda) function, received type: "%s"' % type( callback_method ) )

        if event_name in self._listeners and callback_method in self._listeners[ event_name ]:
            self._listeners[ event_name ].remove( callback_method )
            if len( self._listeners[ event_name ] is 0 ):
                del self._listeners[ event_name ]

    def dispatch( self, event_name, *args, **kvargs ):
        '''
        Dispatch an event to all subscribed listeners.
        '''

        stop_priority = -1
        if event_name in self._listeners:
            for callback_method, priority, counter in self._listeners[ event_name ]:
                if priority >= stop_priority:
                    ret = callback_method( *args, **kvargs )
                    if ret is Dispatcher.STOP_PROPAGATION_IMMEDIATELY:
                        break
                    elif ret is Dispatcher.STOP_PROPAGATION_PRIORITY and priority > stop_priority:
                        stop_priority = priority
                else:
                    break
