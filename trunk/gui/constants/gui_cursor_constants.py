# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#----------------------
# GUI CURSOR CONSTANTS
#----------------------

class GuiCursorConstants( object ):
    '''
    Static class for generating tkinter events.
    '''

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    # available cursors

    INHERITED           = ''
    X_CURSOR            = 'X_cursor'
    ARROW               = 'arrow'
    DOUBLE_ARROW        = 'double_arrow'
    TOP_LEFT_ARROW      = 'top_left_arrow'
    BASED_ARROW_DOWN    = 'based_arrow_down'
    BASED_ARROW_UP      = 'based_arrow_up'
    BOAT                = 'boat'
    BOGOSITY            = 'bogosity'
    TOP_LEFT_CORNER     = 'top_left_corner'
    TOP_RIGHT_CORNER    = 'top_right_corner'
    BOTTOM_LEFT_CORNER  = 'bottom_left_corner'
    BOTTOM_RIGHT_CORNER = 'bottom_right_corner'
    LEFT_SIDE           = 'left_side'
    TOP_SIDE            = 'top_side'
    RIGHT_SIDE          = 'right_side'
    BOTTOM_SIDE         = 'bottom_side'
    LEFT_TEE            = 'left_tee'
    TOP_TEE             = 'top_tee'
    RIGHT_TEE           = 'right_tee'
    BOTTOM_TEE          = 'bottom_tee'
    LEFT_PTR            = 'left_ptr'
    CENTER_PTR          = 'center_ptr'
    RIGHT_PTR           = 'right_ptr'
    CROSS               = 'cross'
    CROSS_REVERSE       = 'cross_reverse'
    CROSSHAIR           = 'crosshair'
    DIAMOND_CROSS       = 'diamond_cross'
    IRON_CROSS          = 'iron_cross'
    TCROSS              = 'tcross'
    DRAFT_LARGE         = 'draft_large'
    DRAFT_SMALL         = 'draft_small'
    HAND1               = 'hand1'
    HAND2               = 'hand2'
    LEFTBUTTON          = 'leftbutton'
    MIDDLEBUTTON        = 'middlebutton'
    RIGHTBUTTON         = 'rightbutton'
    LL_ANGLE            = 'll_angle'
    LR_ANGLE            = 'lr_angle'
    UL_ANGLE            = 'ul_angle'
    UR_ANGLE            = 'ur_angle'
    SB_DOWN_ARROW       = 'sb_down_arrow'
    SB_LEFT_ARROW       = 'sb_left_arrow'
    SB_RIGHT_ARROW      = 'sb_right_arrow'
    SB_UP_ARROW         = 'sb_up_arrow'
    SB_H_DOUBLE_ARROW   = 'sb_h_double_arrow'
    SB_V_DOUBLE_ARROW   = 'sb_v_double_arrow'
    BOX_SPIRAL          = 'box_spiral'
    CIRCLE              = 'circle'
    CLOCK               = 'clock'
    COFFEE_MUG          = 'coffee_mug'
    DOT                 = 'dot'
    DOTBOX              = 'dotbox'
    DRAPED_BOX          = 'draped_box'
    EXCHANGE            = 'exchange'
    FLEUR               = 'fleur'
    GOBBLER             = 'gobbler'
    GUMBY               = 'gumby'
    HEART               = 'heart'
    ICON                = 'icon'
    MAN                 = 'man'
    MOUSE               = 'mouse'
    PENCIL              = 'pencil'
    PIRATE              = 'pirate'
    PLUS                = 'plus'
    QUESTION_ARROW      = 'question_arrow'
    RTL_LOGO            = 'rtl_logo'
    SAILBOAT            = 'sailboat'
    SHUTTLE             = 'shuttle'
    SIZING              = 'sizing'
    SPIDER              = 'spider'
    SPRAYCAN            = 'spraycan'
    STAR                = 'star'
    TARGET              = 'target'
    TREK                = 'trek'
    UMBRELLA            = 'umbrella'
    WATCH               = 'watch'
    XTERM               = 'xterm'

    # OSX native cursors

    OSX_COPY_ARROW                = 'copyarrow'
    OSX_ALIAS_ARROW               = 'aliasarrow'
    OSX_CONTEXTUAL_MENU_ARROW     = 'contextualmenuarrow'
    OSX_CLOSED_HAND               = 'closedhand'
    OSX_OPEN_HAND                 = 'openhand'
    OSX_POINTING_HAND             = 'pointinghand'
    OSX_COUNTING_UP_HAND          = 'countinguphand'
    OSX_COUNTING_DOWN_HAND        = 'countingdownhand'
    OSX_COUNTING_UP_AND_DOWN_HAND = 'countingupanddownhand'
    OSX_RESIZE_LEFT               = 'resizeleft'
    OSX_RESIZE_RIGHT              = 'resizeright'
    OSX_RESIZE_LEFT_RIGHT         = 'resizeleftright'
    OSX_RESIZE_UP                 = 'resizeup'
    OSX_RESIZE_DOWN               = 'resizedown'
    OSX_RESIZE_UP_DOWN            = 'resizeupdown'
    OSX_TEXT                      = 'text'
    OSX_CROSSHAIR                 = 'cross-hair'
    OSX_NONE                      = 'none'
    OSX_NOT_ALLOWED               = 'notallowed'
    OSX_POOF                      = 'poof'
    OSX_SPINNING                  = 'spinning'
    OSX_IBEAM                     = 'ibeam'

    OSX_NATIVES = (
        OSX_COPY_ARROW,
        OSX_ALIAS_ARROW,
        OSX_CONTEXTUAL_MENU_ARROW,
        OSX_CLOSED_HAND,
        OSX_OPEN_HAND,
        OSX_POINTING_HAND,
        OSX_COUNTING_UP_HAND,
        OSX_COUNTING_DOWN_HAND,
        OSX_COUNTING_UP_AND_DOWN_HAND,
        OSX_RESIZE_LEFT,
        OSX_RESIZE_RIGHT,
        OSX_RESIZE_LEFT_RIGHT,
        OSX_RESIZE_UP,
        OSX_RESIZE_DOWN,
        OSX_RESIZE_UP_DOWN,
        OSX_TEXT,
        OSX_CROSSHAIR,
        OSX_NONE,
        OSX_NOT_ALLOWED,
        OSX_POOF,
        OSX_SPINNING,
        OSX_IBEAM,
    )

    # Windows native cursors

    WIN_SIZE       = 'size'
    WIN_SIZE_NE_SW = 'size_ne_sw'
    WIN_SIZE_NS    = 'size_ns'
    WIN_SIZE_NW_SE = 'size_nw_se'
    WIN_SIZE_WE    = 'size_we'
    WIN_NONE       = 'no'
    WIN_STARTING   = 'starting'
    WIN_UP_ARROW   = 'uparrow'
    WIN_WAIT       = 'wait'
    WIN_IBEAM      = 'ibeam'

    WIN_NATIVES = (
        WIN_SIZE,
        WIN_SIZE_NE_SW,
        WIN_SIZE_NS,
        WIN_SIZE_NW_SE,
        WIN_SIZE_WE,
        WIN_NONE,
        WIN_STARTING,
        WIN_UP_ARROW,
        WIN_WAIT,
        WIN_IBEAM,
    )

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
