# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

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
