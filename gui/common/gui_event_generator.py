# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#---------
# IMPORTS
#---------

# custom
from core.gui.constants.gui_event_constants import ComponentEventConstants as CC
from core.gui.constants.gui_event_constants import MouseEventConstants as MC
from core.gui.constants.gui_event_constants import KeyboardEventConstants as KC

#---------------------
# GUI EVENT GENERATOR
#---------------------

class GuiEventGenerator( object ):
    '''
    Static class for generating tkinter events.
    '''

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    _LONG_EVENT_STRAT_CHAR     = '<'
    _LONG_EVENT_DELIMITER_CHAR = '-'
    _LONG_EVENT_END_CHAR       = '>'

    _VALID_TYPES = (
        # component
        CC.ACTIVATE,
        CC.DEACTIVATE,
        CC.DESTROY,
        CC.UPDATE,
        CC.FOCUS_IN,
        CC.FOCUS_OUT,
        # keyboard
        KC.PRESS,
        KC.RELEASE,
        # mouse
        MC.PRESS,
        MC.RELEASE,
        MC.ENTER,
        MC.LEAVE,
        MC.WHEEL,
        MC.MOTION,
    )

    _VALID_MODIFIERS = (
        # keyboard
        KC.CONTROL,
        KC.ALT,
        KC.COMMAND,
        KC.OPTION,
        KC.SHIFT,
        KC.LOCK,
        KC.EXTENDED,
        KC.META,
        #'Mod1',
        #'Mod2',
        #'Mod3',
        #'Mod4',
        #'Mod5',
        # mouse
        MC.DOUBLE,
        MC.TRIPLE,
        MC.QUADRUPLE,
        MC.LEFT_BUTTON,
        MC.MIDDLE_BUTTON,
        MC.RIGHT_BUTTON,
        MC.FOURTH_BUTTON,
        MC.FIFTH_BUTTON,
    )

    _MODIFIER_REPLACEMENTS = {
        MC.LEFT_BUTTON:   'Button1',
        MC.MIDDLE_BUTTON: 'Button2',
        MC.RIGHT_BUTTON:  'Button3',
        MC.FOURTH_BUTTON: 'Button4',
        MC.FIFTH_BUTTON:  'Button5',
    }

    _DETAIL_REPLACEMENTS = {
        ' ': 'space',
        '<': 'less',
    }

    _VALID_DETAIL_MODIFIERS = (
        KC.LEFT,
        KC.RIGHT,
    )

    _DETAIL_MODIFIABLE_TYPES = (
        KC.PRESS,
        KC.RELEASE,
    )

    _MODIFIABLE_DETAILS = (
        KC.SHIFT,
        KC.ALT,
        KC.CONTROL,
        KC.COMMAND,
        KC.OPTION,
    )

    #-----------------------
    # PUBLIC STATIC METHODS
    #-----------------------

    @staticmethod
    def get_event_string( event_type, event_modifiers = None, event_detail = None, detail_modifier = None ):
        '''
        Creates tkinter event string trying to ensure valid parts.
        '''

        event_parts = GuiEventGenerator._prepare_values( event_type, event_modifiers )

        if event_detail is not None:
            event_detail = GuiEventGenerator._prepare_detail( event_type, event_detail, detail_modifier )
            event_parts.append( event_detail )

        return GuiEventGenerator._pack_event( event_parts )

    #------------------------
    # PRIVATE STATIC METHODS
    #------------------------

    @staticmethod
    def _prepare_values( event_type, event_modifiers ):
        '''
        Ensures that given values are all valid.
        '''

        if not event_type in GuiEventGenerator._VALID_TYPES:
            raise RuntimeError( 'Event type "%s" is not valid!' % event_type )
        if not event_modifiers:
            return [ event_type ]

        event_modifiers = list( event_modifiers )
        for index, modifier in enumerate( event_modifiers ):

            if not modifier in GuiEventGenerator._VALID_MODIFIERS:
                raise RuntimeError( 'Event modifier "%s" is not valid!' % modifier )

            if modifier in GuiEventGenerator._MODIFIER_REPLACEMENTS:
                event_modifiers[ index ] = GuiEventGenerator._MODIFIER_REPLACEMENTS[ modifier ]

        event_modifiers.append( event_type )
        return event_modifiers

    @staticmethod
    def _prepare_detail( event_type, event_detail, detail_modifier ):
        '''
        Processes optional detail modifier.
        '''

        if event_detail in GuiEventGenerator._DETAIL_REPLACEMENTS:
            event_detail = GuiEventGenerator._DETAIL_REPLACEMENTS[ event_detail ]

        if detail_modifier is not None:

            if event_type in GuiEventGenerator._DETAIL_MODIFIABLE_TYPES:

                if detail_modifier in GuiEventGenerator._VALID_DETAIL_MODIFIERS:

                    if event_detail in GuiEventGenerator._MODIFIABLE_DETAILS:

                        event_detail += detail_modifier

                    else:
                        raise RuntimeError( 'Event detail "%s" is not modifiable!' % event_detail )
                    
                else:
                    raise RuntimeError( 'Invalid detail modifier for event type "%s"!' % event_type )

            else:
                raise RuntimeError( 'Only keyboard press and release events may have detail modifiers! Event is "%s".' % event_type )

        return event_detail

    @staticmethod
    def _pack_event( event_parts ):
        '''
        Packages event_parts joining them with '-' and placing the result between '<' and '>'.
        '''

        return GuiEventGenerator._LONG_EVENT_STRAT_CHAR + GuiEventGenerator._LONG_EVENT_DELIMITER_CHAR.join( event_parts ) + GuiEventGenerator._LONG_EVENT_END_CHAR

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
