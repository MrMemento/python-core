# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

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
