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
from Tkinter import *

# custom
from core.constants.sys_constants import SysConstants as SC
from core.constants.protocol_constants import ProtocolConstants as PC
from core.constants.event_constants import EventConstants as EC

from core.utils.dispatcher import Dispatcher
from core.utils.importer import Importer
from core.utils.script_formater import ScriptFormater
from core.utils.runtime_class import RuntimeClass
from core.utils.logger import LoggerUser

from core.gui.constants.gui_descriptor_constants import GuiDescriptorConstants as GDC
from core.gui.constants.gui_config_constants import GuiConfigConstants as GCC
from core.gui.constants.gui_event_constants import ComponentEventConstants as CC
from core.gui.constants.gui_event_constants import MouseEventConstants as MC
from core.gui.constants.gui_event_constants import KeyboardEventConstants as KC

from core.gui.common.gui_component import GuiComponent
from core.gui.common.gui_event_generator import GuiEventGenerator

from core.gui.managers.mouse_manager import MouseManager
from core.gui.managers.keyboard_manager import KeyboardManager

from core.gui.components.statusbar import StatusBar
from core.gui.components.wrapped_label import WrappedLabel
from core.gui.components.scrollable_frame import ScrollableFrame

#-------------
# GUI FACTORY
#-------------

class GuiFactory( LoggerUser ):
    '''
    Class for building GUI out of JSON descriptor.
    '''

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    _WM_DELETE_WINDOW        = 'WM_DELETE_WINDOW'
    _GEOMETRY_STRING         = '%dx%d%+d%+d'
    _ACCELERATOR_DELIMITER   = '+'
    _COMPONENT_CLASS_POSTFIX = 'Component'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self, operating_system, translator_function = None, dispatcher = None ):
        '''
        Constructor.
        '''

        #-------------------
        # PRIVATE VARIABLES
        #-------------------

        self._os            = operating_system
        self._translator    = translator_function
        self._loaded        = False
        self._initialized   = False
        self._descriptor    = None
        self._gui_root      = None
        self._container     = None
        self._controllers   = [ ]
        self._states        = None
        self._current_state = None
        if dispatcher:
            self._dispatcher = dispatcher
        else:
            self._dispatcher = Dispatcher( )

        MouseManager.set_os( operating_system )
        KeyboardManager.set_os( operating_system )

    #-------------------
    # PUBLIC PROPERTIES
    #-------------------

    @property
    def dispatcher( self ):
        '''
        Return the dispatcher instance.
        '''

        return self._dispatcher

    #----------------
    # PUBLIC METHODS
    #----------------

    def load_descriptor( self, descriptor_or_path, **kvargs ):
        '''
        Loads descriptor object from path or URL.
        Default behaviour is loading from URL, can be overridden with kvarg "protocol".
        Use presented static constants in "ProtocolConstants".
        '''

        if self._loaded:
            raise RuntimeError( '"GuiFactory::gui_load_descriptor( )" already loaded!' )

        if isinstance( descriptor_or_path, dict ):

            self._descriptor = descriptor_or_path

        elif isinstance( descriptor_or_path, str ):

            if kvargs.has_key( PC.PROTOCOL ) and kvargs[ PC.PROTOCOL ] == PC.FILE_PROTOCOL:
                data_source = open( descriptor_or_path )
            else:
                data_source = urllib2.urlopen( urllib2.Request( url = descriptor_or_path ) )

            json_data = data_source.read( )
            data_source.close( )

            # format json string, this way there may be comments in it for developers
            # be sure, to first remove comments, than new lines!
            json_data = ScriptFormater.remove_comments( json_data )
            json_data = ScriptFormater.remove_empty_lines( json_data )
            #print( json_data )

            self._descriptor = json.loads( json_data )

        else:

            raise RuntimeError( '"GuiFactory::gui_load_descriptor( )" accepts only dictionary or path/url string! presented type is %s' % type( dictionary_or_path ) )

        self._loaded = True

    def initialize( self ):
        '''
        Initializes TK GUI main window.
        '''

        #--------
        # checks
        #--------

        if not self._loaded:
            raise RuntimeError( '"GuiFactory" descriptor not loaded! Use "GuiFactory::gui_load_descriptor( )" function first!' )
        if self._initialized:
            raise RuntimeError( '"GuiFactory::gui_initialize( )" already initialized!' )

        #--------
        # basics
        #--------

        self._gui_root = Tk( )
        self._gui_root.protocol( GuiFactory._WM_DELETE_WINDOW, self.destroy )
        MouseManager.set_root( self._gui_root )

        #-----------------------------------
        # main settings based on descriptor
        #-----------------------------------

        # main window
        self._set_geometry( self._gui_root, self._descriptor[ GDC.APPLICATION ] )
        self._set_resizability( self._gui_root, self._descriptor[ GDC.APPLICATION ] )

        # main window title
        if self._descriptor[ GDC.APPLICATION ].has_key( GDC.TITLE ):
            self._set_title( self._gui_root, self._descriptor[ GDC.APPLICATION ][ GDC.TITLE ] )
        else:
            raise RuntimeError( 'No window title presented in descriptor!' )

        # main window menu
        if self._descriptor[ GDC.APPLICATION ].has_key( GDC.MENU ):
            self._set_menu( self._gui_root, self._descriptor[ GDC.APPLICATION ][ GDC.MENU ] )

        # main window statusbar
        if self._descriptor[ GDC.APPLICATION ].has_key( GDC.STATUSBAR ):
            self._set_statusbar( self._gui_root, self._descriptor[ GDC.APPLICATION ][ GDC.STATUSBAR ] )

        # create container frame
        self._container = Frame( self._gui_root,
            #background = 'black'
        )
        self._container.pack(
            fill   = BOTH,
            expand = True
        )

        # build available states
        if self._descriptor[ GDC.APPLICATION ].has_key( GDC.STATES ):
            self._states = self._build_states( self._container, self._descriptor[ GDC.APPLICATION ][ GDC.STATES ] )
        else:
            raise RuntimeError( 'No states are presented in descriptor!' )

        # set initialized flag
        self._initialized = True

    def start( self ):
        '''
        Starts GUI infinite loop, from this point on only event based codes will run.
        '''

        self._check_dependencies( )

        self._dispatcher.add_listener( EC.KILL,       self.destroy )
        self._dispatcher.add_listener( EC.SHOW_STATE, self.show_state )

        self._gui_root.mainloop( )

    def show_state( self, state_name = GDC.STATE_DEFAULT ):
        '''
        Show described GUI frame from descriptor.
        '''

        self._check_dependencies( )
        if not self._states.has_key( state_name ):
            raise RuntimeError( 'Specified state does not exist in built states: "%s"' % state_name )

        if not self._current_state is None:

            self.log( 'Destroying state: "%s"' % self._current_state )

            self._states[ self._current_state ].pack_forget( )
            self._dispatcher.dispatch( EC.STATE_HIDDEN, self._current_state )

        self.log( 'Showing state: "%s"' % state_name )

        self._states[ state_name ].pack(
            fill   = BOTH,
            expand = True
        )
        self._gui_root.update_idletasks( )
        self._current_state = state_name

        self._dispatcher.dispatch( EC.STATE_SHOWN, state_name )

    def destroy( self ):
        '''
        Kills GUI infinite loop, and destroys all widgets.
        '''

        self._check_dependencies( )
        self._gui_root.destroy( )

        self._initialized = False

    def translate( self, label ):
        '''
        Translator function, if translator function is set.
        '''

        if self._translator is not None:
            return self._translator( label )
        else:
            return label

    #-----------------
    # PRIVATE METHODS
    #-----------------

    def _check_dependencies( self ):
        '''
        Checker function for loaded descriptor and initialized GUI.
        If any of the above is missing, raises RuntimeError.
        '''

        if not self._loaded:
            raise RuntimeError( '"GuiFactory" descriptor not loaded! Use "GuiFactory::gui_load_descriptor( )" function first!' )
        elif not self._initialized:
            raise RuntimeError( '"GuiFactory" not initialized! Use "GuiFactory::gui_initialize( )" function first!' )

    def _percent_to_num( self, value ):
        '''
        Checks a string if it is a valid percent value.
        Returns numeric representation if so. [0;1]
        '''

        if value.endswith( '%' ):
            value = value[ 0 : -1 ]

        value = int( value ) *0.01
        return value

    def _get_component( self, Class, *args, **kvargs ):
        '''
        Create a new instance inherited from "Class" decorated with GuiComponent class' methods.
        '''

        return RuntimeClass.get_decorated_instance(
            Class.__name__ + GuiFactory._COMPONENT_CLASS_POSTFIX,
            Class, GuiComponent,
            *args, **kvargs
        )

    def _create_controller( self, path ):
        '''
        Import and instantiate controller class based on descriptor.
        '''

        ControllerClass = Importer.import_by_path( path )
        controller      = ControllerClass( self._dispatcher, self._gui_root, self._os, self._translator )
        self._controllers.append( controller )

        return controller

    def _set_title( self, tk_instance, label ):
        '''
        Sets title of TK instance.
        '''

        tk_instance.title( self.translate( label ) )

    def _set_geometry( self, tk_instance, descriptor ):
        '''
        Sets geometry of TK instance.
        '''

        width      = GDC.DEFAULT_WIDTH
        height     = GDC.DEFAULT_HEIGHT
        offset_x   = GDC.DEFAULT_OFFSET_X
        offset_y   = GDC.DEFAULT_OFFSET_Y
        win_width  = tk_instance.winfo_screenwidth( )
        win_height = tk_instance.winfo_screenheight( )

        if descriptor.has_key( GDC.WIDTH ):

            w = descriptor[ GDC.WIDTH ]
            if isinstance( w, int ):
                width = w
            elif isinstance( w, str ) or isinstance( w, unicode ):
                w     = self._percent_to_num( w )
                width = win_width * w

        if descriptor.has_key( GDC.HEIGHT ):

            h = descriptor[ GDC.HEIGHT ]
            if isinstance( h, int ):
                height = h
            elif isinstance( h, str ) or isinstance( h, unicode ):
                h      = self._percent_to_num( h )
                height = win_height * h

        if descriptor.has_key( GDC.OFFSET_X ):

            ox = descriptor[ GDC.OFFSET_X ]
            if isinstance( ox, int ):
                offset_x = ox
            elif isinstance( ox, str ) or isinstance( ox, unicode ):
                ox       = self._percent_to_num( ox )
                offset_x = ( win_width - width ) * ox

        if descriptor.has_key( GDC.OFFSET_Y ):

            oy = descriptor[ GDC.OFFSET_Y ]
            if isinstance( oy, int ):
                offset_y = oy
            elif isinstance( oy, str ) or isinstance( oy, unicode ):
                oy       = self._percent_to_num( oy )
                offset_y = ( win_height - height ) * oy

        tk_instance.geometry( GuiFactory._GEOMETRY_STRING % ( width, height, offset_x, offset_y ) )

    def _set_resizability( self, tk_instance, descriptor ):
        '''
        Sets resizibility of TK instance.
        '''

        if descriptor.has_key( GDC.RESIZABLE ) and isinstance( descriptor[ GDC.RESIZABLE ], bool ):
            tk_instance.resizable(
                descriptor[ GDC.RESIZABLE ],
                descriptor[ GDC.RESIZABLE ]
            )
            if not descriptor[ GDC.RESIZABLE ]:
                return

        if descriptor.has_key( GDC.MIN_WIDTH ) and isinstance( descriptor[ GDC.MIN_WIDTH ], int ) and descriptor.has_key( GDC.MIN_HEIGHT ) and isinstance( descriptor[ GDC.MIN_HEIGHT ], int ):
            tk_instance.minsize( descriptor[ GDC.MIN_WIDTH ], descriptor[ GDC.MIN_HEIGHT ] )

        if descriptor.has_key( GDC.MAX_WIDTH ) and isinstance( descriptor[ GDC.MAX_WIDTH ], int ) and descriptor.has_key( GDC.MAX_HEIGHT ) and isinstance( descriptor[ GDC.MAX_HEIGHT ], int ):
            tk_instance.maxsize( descriptor[ GDC.MAX_WIDTH ], descriptor[ GDC.MAX_HEIGHT ] )

    def _set_menu( self, master, descriptor ):
        '''
        Creates menu in presented tk_menu_base.
        '''

        # ensure contained items
        if not descriptor.has_key( GDC.ITEMS ):
            raise RuntimeError( 'No items found in menu structure!' )

        #-----------------------------------------
        # recursive menu builder function - start
        #-----------------------------------------

        def _create_menu_structure( menu_base, menu_descriptor, menu_controller, root ):

            for item in menu_descriptor:

                if not item.has_key( GDC.TYPE ):
                    raise RuntimeError( 'Processed menu item has no key "%s"!' % GDC.TYPE )

                if item[ GDC.TYPE ] == GDC.SEPARATOR:

                    #-----------
                    # separator
                    #-----------

                    menu_base.add_separator( )

                elif item[ GDC.TYPE ] == GDC.CONTAINER:

                    #-----------
                    # container
                    #-----------

                    if not item.has_key( GDC.LABEL ):
                        raise RuntimeError( 'Processed menu item has no key "%s"!' % GDC.LABEL )
                    elif not item.has_key( GDC.ITEMS ):
                        raise RuntimeError( 'Processed menu container has no key "%s"!' % GDC.ITEMS )
                    elif len( item[ GDC.ITEMS ] ) == 0:
                        raise RuntimeError( 'Processed menu container has no items!' )

                    tearoff = False
                    if item.has_key( GDC.TEAROFF ):
                        tearoff = item[ GDC.TEAROFF ]

                    menu_component = self._get_component(
                        Menu, menu_base,
                        tearoff = tearoff
                    )
                    menu_controller.register_component( menu_component )

                    _create_menu_structure( menu_component, item[ GDC.ITEMS ], menu_controller, root )

                    menu_base.add_cascade(
                        label = self.translate( item[ GDC.LABEL ] ),
                        menu  = menu_component
                    )

                elif item[ GDC.TYPE ] == GDC.COMMAND:

                    #---------
                    # command
                    #---------

                    if not item.has_key( GDC.LABEL ):
                        raise RuntimeError( 'Processed menu item has no key "%s"!' % GDC.LABEL )
                    elif not item.has_key( GDC.CALLBACK ):
                        raise RuntimeError( 'Processed menu command has no key "%s"!' % GDC.CALLBACK )
                    elif not hasattr( controller, item[ GDC.CALLBACK ] ):
                        raise RuntimeError( 'Processed menu command "%s" is not found in controller "%s"!' % ( item[ GDC.CALLBACK ], menu_controller.__class__.__name__ ) )

                    callback    = getattr( controller, item[ GDC.CALLBACK ] )
                    accelerator = None
                    if item.has_key( GDC.ACCELERATOR ):
                        accelerator = item[ GDC.ACCELERATOR ]

                    menu_base.add_command(
                        label       = self.translate( item[ GDC.LABEL ] ),
                        command     = callback,
                        accelerator = accelerator
                    )

                    if accelerator is not None:

                        accelerator_parts = accelerator.split( GuiFactory._ACCELERATOR_DELIMITER )
                        if len( accelerator_parts ) < 2:
                            raise RuntimeError( 'Menu accelerator format is invalid. Use at least one modifier and the detail (character)! (Provided: "%s")' % accelerator )
                        detail = accelerator_parts.pop( )
                        event  = GuiEventGenerator.get_event_string(
                            KC.PRESS,
                            accelerator_parts,
                            detail
                        )

                        master.bind_all( event, callback )
                        pass

                else:

                    raise RuntimeError( 'Processed menu item type "%s" is not valid or not yet implemented!' % item[ GDC.TYPE ] )

        #---------------------------------------
        # recursive menu builder function - end
        #---------------------------------------

        if not descriptor.has_key( GDC.CONTROLLER ):
            raise RuntimeError( 'Controller class not present in menu descriptor!' )

        controller = self._create_controller( descriptor[ GDC.CONTROLLER ] )
        root_menu  = self._get_component(
            Menu, master,
            tearoff = False
        )
        controller.register_component( root_menu )

        _create_menu_structure( root_menu, descriptor[ GDC.ITEMS ], controller, master )

        master.config(
            menu = root_menu
        )

        # TODO:
        # create left click (context) menu

    def _set_statusbar( self, master, descriptor ):
        '''
        Add statusbar to component.
        '''

        if not descriptor.has_key( GDC.CONTROLLER ):
            raise RuntimeError( 'Controller class not present in statusbar descriptor!' )

        controller = self._create_controller( descriptor[ GDC.CONTROLLER ] )
        bar        = self._get_component(
            StatusBar, master
        )
        bar.pack( )

        controller.register_component( bar )

    def _build_states( self, container, states_dict ):
        '''
        Build available states based on descriptor.
        Returns a dictionary containing keys from descriptor, and its values are non-packed frames with "container" set as their parent.
        '''

        states     = { }
        descriptor = None
        for state in states_dict:

            self.log( 'Building state: "%s"' % state )

            descriptor = states_dict[ state ]
            if not descriptor.has_key( GDC.CONTROLLER ):
                raise RuntimeError( 'Controller class not present in application state descriptor "%s"!' % state )
            if not descriptor.has_key( GDC.COMPONENTS ) or len( descriptor[ GDC.COMPONENTS ] ) is 0:
                raise RuntimeError( 'No components found in application state descriptor "%s"!' % state )

            controller      = self._create_controller( descriptor[ GDC.CONTROLLER ] )
            states[ state ] = Frame( container )
            self._build_components( states[ state ], descriptor[ GDC.COMPONENTS ], controller )

        return states

    def _build_components( self, master, descriptor, controller ):
        '''
        Component builder function to be used recursively.
        '''

        for component in descriptor:

            if not component.has_key( GDC.TYPE ):
                raise RuntimeError( 'Component description lacks configuration options "%s"!' % GDC.TYPE )
            if not component.has_key( GDC.CONFIG ):
                raise RuntimeError( 'Component description lacks configuration options "%s"!' % GDC.CONFIG )
            if not component.has_key( GDC.GEOMETRY ):
                raise RuntimeError( 'Component description lacks geometry options "%s"' % GDC.GEOMETRY )

            self.sub( 'Building component: "%s"' % component[ GDC.TYPE ] )

            config, callback = self._manage_config( component[ GDC.CONFIG ], controller )
            geometry         = self._manage_geometry( component[ GDC.GEOMETRY ] )

            try:

                instance = self._get_component(
                    {
                        GDC.LABEL:            Label,
                        GDC.BUTTON:           Button,
                        GDC.WRAPPED_LABEL:    WrappedLabel,
                        GDC.SCROLLABLE_FRAME: ScrollableFrame,
                    }[ component[ GDC.TYPE ] ],
                    master,
                    **config
                )

                if not callback is None:

                    # add target to callback arguments
                    command = lambda *args, **kvargs: callback( instance, *args, **kvargs )
                    instance.config(
                        command = command
                    )

                instance.pack( **geometry )

                controller.register_component( instance )

                # - CONTENT (optional)

                if component.has_key( GDC.CONTENT ):

                    if not component[ GDC.CONTENT ].has_key( GDC.TYPE ):
                        raise RuntimeError( 'Content description lacks configuration options "%s"!' % GDC.TYPE )
                    if not component[ GDC.CONTENT ].has_key( GDC.CONFIG ):
                        raise RuntimeError( 'Content description lacks configuration options "%s"!' % GDC.CONFIG )

                    try:

                        config, callback = self._manage_config( component[ GDC.CONTENT ][ GDC.CONFIG ], controller )

                        content = self._get_component(
                            {
                                GDC.LISTBOX: Listbox
                            }[ component[ GDC.CONTENT ][ GDC.TYPE ] ],
                            instance,
                            **config
                        )
                        instance.attach_widget( content )
                        controller.register_component( content )

                    except KeyError, e:
                        raise RuntimeError( 'Content type not yet implemented: "%s"' % component[ GDC.CONTENT ] )

                # - ITEMS (optional)

                #if component.has_key( GDC.ITEMS ):
                    #print( component[ GDC.ITEMS ] )

            except KeyError, e:
                raise RuntimeError( 'Component type not yet implemented: "%s"' % component[ GDC.TYPE ] )

    def _manage_config( self, config, controller ):
        '''
        Function for processing configuration keys.
        Returns a tuple of config dictionary and extracted callback function, if present (None otherwise).
        Extraction of callback is needed to pass instance as target argument to command.
        '''

        if config.has_key( GDC.TEXT ):
            config[ GDC.TEXT ] = self.translate( config[ GDC.TEXT ] )

        if config.has_key( GDC.ANCHOR ):
            config[ GDC.ANCHOR ] = GCC.ANCHOR_REPLACEMENTS[ config[ GDC.ANCHOR ] ]

        if config.has_key( GDC.RELIEF ):
            config[ GDC.RELIEF ] = GCC.RELIEF_REPLACEMENTS[ config[ GDC.RELIEF ] ]

        if config.has_key( GDC.JUSTIFY ):
            config[ GDC.JUSTIFY ] = GCC.JUSTIFY_REPLACEMENTS[ config[ GDC.JUSTIFY ] ]

        if config.has_key( GDC.STATE ):
            config[ GDC.STATE ] = GCC.STATE_REPLACEMENTS[ config[ GDC.STATE ] ]

        if config.has_key( GDC.SELECTMODE ):
            config[ GDC.SELECTMODE ] = GCC.SELECTMODE_REPLACEMENTS[ config[ GDC.SELECTMODE ] ]

        callback = None
        if config.has_key( GDC.CALLBACK ):
            callback = getattr( controller, config[ GDC.CALLBACK ] )
            del config[ GDC.CALLBACK ]

        return config, callback

    def _manage_geometry( self, geometry ):
        '''
        Function for processing geometry keys.
        '''

        if geometry.has_key( GDC.FILL ):
            geometry[ GDC.FILL ] = GCC.FILL_REPLACEMENTS[ geometry[ GDC.FILL ] ]

        if geometry.has_key( GDC.SIDE ):
            geometry[ GDC.SIDE ] = GCC.SIDE_REPLACEMENTS[ geometry[ GDC.SIDE ] ]

        return geometry
