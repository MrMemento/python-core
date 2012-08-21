# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#--------------------------
# GUI DESCRIPTOR CONSTANTS
#--------------------------

class GuiDescriptorConstants( object ):
    '''
    Static class holding gui descriptor regarding constants.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    # defaults
    DEFAULT_TITLE    = 'Window Title'
    DEFAULT_WIDTH    = 320
    DEFAULT_HEIGHT   = 240
    DEFAULT_OFFSET_X = 0
    DEFAULT_OFFSET_Y = 0

    # common
    APPLICATION = 'application'
    TITLE       = 'title'
    LABEL       = 'label'
    TEXT        = 'text'
    ITEMS       = 'items'
    CONTROLLER  = 'controller'
    CONFIG      = 'config'
    GEOMETRY    = 'geometry'
    ANCHOR      = 'anchor'
    RELIEF      = 'relief'
    TYPE        = 'type'
    STATE       = 'state'
    CONTENT     = 'content'

    # geometry
    FILL       = 'fill'
    SIDE       = 'side'
    RESIZABLE  = 'resizable'
    MIN_WIDTH  = 'min_width'
    MIN_HEIGHT = 'min_height'
    MAX_WIDTH  = 'max_width'
    MAX_HEIGHT = 'max_height'
    WIDTH      = 'width'
    HEIGHT     = 'height'
    OFFSET_X   = 'offset_x'
    OFFSET_Y   = 'offset_y'
    SELECTMODE = 'selectmode'

    # menu
    MENU        = 'menu'
    TYPE        = 'type'
    COMMAND     = 'command'
    CONTAINER   = 'container'
    ARGS        = 'args'
    KVARGS      = 'kvargs'
    TEAROFF     = 'tearoff'
    CALLBACK    = 'callback'
    SEPARATOR   = 'separator'
    ACCELERATOR = 'accelerator'

    # widget names
    STATUSBAR        = 'statusbar'
    BUTTON           = 'button'
    LABEL            = 'label'
    LISTBOX          = 'listbox'
    WRAPPED_LABEL    = 'wrapped_label'
    SCROLLABLE_FRAME = 'scrollable_frame'

    # states
    STATES        = 'states'
    STATE_DEFAULT = 'default'
    COMPONENTS    = 'components'

    # text
    JUSTIFY = 'justify'

    # dialogs
    FILE_OPEN_DIALOG      = 'file_open'
    DIRECTORY_OPEN_DIALOG = 'directory_open'
    FILE_SAVE_DIALOG      = 'file_save'
    YES_NO_DIALOG         = 'yes_no'
    OK_CANCEL_DIALOG      = 'ok_cancel'
    RETRY_CANCEL_DIALOG   = 'retry_cancel'
    INFO_DIALOG           = 'info'
    WARNING_DIALOG        = 'warning'
    ERROR_DIALOG          = 'error'
    COLOR_DIALOG          = 'color'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
