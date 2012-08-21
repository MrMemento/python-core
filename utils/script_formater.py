# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#---------
# IMPORTS
#---------

# global
import re

#-----------------
# SCRIPT FORMATER
#-----------------

class ScriptFormater( object ):
    '''
    Class for formating script files.
    '''

    #--------------------------
    # PRIVATE STATIC VARIABLES
    #--------------------------

    _TRIM_PAT_HTML = r'''
        (?:                             ##  various things which are not to be trimmed:
            (?P<nonchar>
                (?<!\\)"                ##      start of " ... " string
                (
                    \\.                 ##              escaped char
                |                       ##          or
                    [^"\\]              ##              non " \ characters
                )*
                "                       ##      end of " ... " string
            |                           ##  or
                (?<!\\)'                ##      start of ' ... ' string
                (                       ##
                    \\.                 ##              escaped char
                |                       ##          or
                    [^'\\]              ##              non '\ characters
                )*
                '                       ##      end of ' ... ' string
            )
        |
            [^\S\n]*
            (?P<char>[%s])
            [^\S\n]*
        )
    '''

    _TRIM_PAT = r'''
        (?:                             ##  various things which are not to be trimmed:
            (?P<nonchar>
                (?<![\\/])/(?![/\*])    ##      start of / ... / string
                (
                    \\.                 ##              escaped char
                |                       ##          or
                    [^/\\\n]            ##              non / \ \n characters
                )+
                /                       ##      end of / ... / string
            |                           ##  or
                (?<!\\)"                ##      start of " ... " string
                (
                    \\.                 ##              escaped char
                |                       ##          or
                    [^"\\]              ##              non " \ characters
                )*
                "                       ##      end of " ... " string
            |                           ##  or
                (?<!\\)'                ##      start of ' ... ' string
                (                       ##
                    \\.                 ##              escaped char
                |                       ##          or
                    [^'\\]              ##              non '\ characters
                )*
                '                       ##      end of ' ... ' string
            )
        |
            [^\S\n]*
            (?P<char>[%s])
            [^\S\n]*
        )
    '''

    _SPACES_OUTSIDE_QUOTES_RE_HTML = re.compile( r'''
        (?:
            (?P<spaces>
                [^\S\n]+                ## spaces and tabs
            )
        |                               ##  or various things which are not to be removed:
            (?P<nonspace>
                (?<!\\)"                ##      start of " ... " string
                (
                    \\.                 ##              escaped char
                |                       ##          or
                    [^"\\]              ##              non " \ characters
                )*
                "                       ##      end of " ... " string
            |                           ##  or
                (?<!\\)'                ##      start of ' ... ' string
                (                       ##
                    \\.                 ##              escaped char
                |                       ##          or
                    [^'\\]              ##              non '\ characters
                )*
                '                       ##      end of ' ... ' string
            |                           ##  or
                [\S\n]+                 ##      chars which are not space or tab
            )
        )
    ''', re.VERBOSE | re.MULTILINE )

    _SPACES_OUTSIDE_QUOTES_RE = re.compile( r'''
        (?:
            (?P<spaces>
                [^\S\n]+                ## spaces and tabs
            )
        |                               ##  or various things which are not to be removed:
            (?P<nonspace>
                (?<![\\/])/(?![/\*])    ##      start of / ... / string
                (
                    \\.                 ##              escaped char
                |                       ##          or
                    [^/\\\n]            ##              non / \ \n characters
                )+
                /                       ##      end of / ... / string
            |                           ##  or
                (?<!\\)"                ##      start of " ... " string
                (
                    \\.                 ##              escaped char
                |                       ##          or
                    [^"\\]              ##              non " \ characters
                )*
                "                       ##      end of " ... " string
            |                           ##  or
                (?<!\\)'                ##      start of ' ... ' string
                (                       ##
                    \\.                 ##              escaped char
                |                       ##          or
                    [^'\\]              ##              non '\ characters
                )*
                '                       ##      end of ' ... ' string
            |                           ##  or
                [\S\n]+                 ##      chars which are not space or tab
            )
        )
    ''', re.VERBOSE | re.MULTILINE )

    _NEWLINES_RE = re.compile( r'''
        (?<=
            [^\\]
        )
        (?:
            [\n\r]+
        )
        (?P<content>.*(?![\n\r]))
    ''', re.VERBOSE )

    _SPACES_RE = re.compile( r'''
        [^\S\n]+
    ''', re.VERBOSE )

    _COMMENT_RE = re.compile( r'''
        (?P<linestart>^)?               ##  is it a linestart
        (?P<before>[^\S\n]*)            ##  any whitespace but newline
        (?:
            /\*                         ##      multiline comment start
            (?P<multicomment>.*?)       ##      content
            \*/                         ##      end
        |                               ##  or
            //                          ##      single line comment start
            (?P<singlecomment>[^\n]*)   ##      content
        |                               ##  or
            (?P<noncomment>             ##      not comment
                (?<![\\/])/(?![/\*])    ##          start of / ... / string
                (
                    \\.                 ##                  escaped char
                |                       ##              or
                    [^/\\\n]            ##                   non / \ \n characters
                )+
                /                       ##          end of / ... / string
            |                           ##      or
                (?<!\\)"                ##      start of " ... " string
                (
                    \\.                 ##              escaped char
                |                       ##          or
                    [^"\\]              ##              non " \ characters
                )*
                "                       ##      end of " ... " string
            |                           ##  or
                (?<!\\)'                ##      start of ' ... ' string
                (                       ##
                    \\.                 ##              escaped char
                |                       ##          or
                    [^'\\]              ##              non '\ characters
                )*
                '                       ##      end of ' ... ' string
            |                           ##  or
                .[^/"'\\]*              ##      anything not comment, escaped char, or string
            )
        )
        (?P<after>[^\S\n]*)             ##  any whitespace but newline
        (?P<lineend>$)?                 ##  is it a lineend
    ''', re.VERBOSE | re.DOTALL | re.MULTILINE )        

    _C_STYLE_COMMENT_RE = re.compile( r'''
        (?:
            /\*                         ##      Start of /* ... */ comment
            [^*]*\*+                    ##      Non-* followed by 1-or-more *'s
            (?:
                [^/*][^*]*\*+
            )*                          ##      0-or-more things which don't start with / but do end with '*'
            /                           ##      End of /* ... */ comment
        |                               ##  or  various things which aren't comments:
            (?P<noncomment>
                (?<![\\/])/(?![/\*])    ##          start of / ... / string
                (
                    \\.                 ##                  escaped char
                |                       ##              or
                    [^/\\\n]            ##                   non / \ \n characters
                )+
                /                       ##          end of / ... / string
            |                           ##      or
                (?<!\\)"                ##      start of " ... " string
                (
                    \\.                 ##              escaped char
                |                       ##          or
                    [^"\\]              ##              non " \ characters
                )*
                "                       ##      end of " ... " string
            |                           ##  or
                (?<!\\)'                ##      start of ' ... ' string
                (                       ##
                    \\.                 ##              escaped char
                |                       ##          or
                    [^'\\]              ##              non '\ characters
                )*
                '                       ##      end of ' ... ' string
            |                           ##  or
                .[^/"'\\]*              ##      chars which doesn't start a comment, string
            )
        )
    ''', re.VERBOSE | re.MULTILINE | re.DOTALL )

    #_HTML_TAG_RE = re.compile( r'''
        #<(?!(\?|!--))                                   ## tag starts with < but not <? or <!--
        #(?P<closing>/?)                                 ## if / here than closing tag
        #(?P<tagname>[^\s:='">]*)                        ## name of the tag if any
        #\:?                                             ## class identifier if any
        #(?P<tagclass>[^\s='">]*)                        ## class if any
        #\s*                                             ## followed by any number of whitespace
        #(?P<attributes>                                 ## any number of attributes
            #(?:
                #[^\s='"/>]*                             ## name of attribute
                #(?:                                     ## do we have any value for that?
                    #\s*=\s*                             ## looking for equal sign
                    #(?:
                        #".*?"                           ##     value between "
                    #|                                   ## or
                        #'.*?'                           ##     value between '
                    #|                                   ## or
                        #[^\s'"/>]*                      ##     word
                    #)\s*
                #)*                                      ## would be stupid to have more values assigned...
            #)*
        #)
        #\s*(?P<selfclosed>/)?                           ## if / here than self closed tag
        #\s*>
    #''', re.VERBOSE )

    #_HTML_TAG_CONT_RE = re.compile( r'''
        #<(?!(\?|!--))                                   ## tag starts with < but not <? or <!--
        #(?P<closing>/?)                                 ## if / here than closing tag
        #(?P<tagname>[^\s:='">]*)                        ## name of the tag if any
        #\:?                                             ## class identifier if any
        #(?P<tagclass>[^\s='">]*)                        ## class if any
        #\s*                                             ## followed by any number of whitespace
        #(?P<attributes>                                 ## any number of attributes
            #(?:
                #[^\s='"/>]*                             ## name of attribute
                #(?:                                     ## do we have any value for that?
                    #\s*=\s*                             ## looking for equal sign
                    #(?:
                        #".*?"                           ##     value between "
                    #|                                   ## or
                        #'.*?'                           ##     value between '
                    #|                                   ## or
                        #[^\s'"/>]*                      ##     word
                    #)
                    #\s*
                #)*                                      ## would be stupid to have more values assigned...
            #)*
        #)
        #\s*
        #(?:
            #(?P<selfclosed>/)                           ##     if / here than self closed tag
            #\s*>                                        ##     tag end  
        #|                                               ## or
            #>                                           ##     tag end
            #(?P<content>                                ##     tag content
                #(?:
                    #\s*
                    #(?:
                        #/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*) ##         comments
                    #|                                   ##     or
                        #".*?"                           ##         value between "
                    #|                                   ##     or
                        #'.*?'                           ##         value between '
                    #|                                   ##     or
                        #\w                              ##         word
                    #)
                    #\s*
                #)*
            #)
            #(?P<closetag>
                #<\s*/\s*
                #(?P=tagname)
                #\s*>
            #)
        #)
    #''', re.VERBOSE )

    #-----------------------
    # PUBLIC STATIC METHODS
    #-----------------------

    @staticmethod
    def remove_empty_lines( text ):
        '''
        Strips multiple lines containing only whitespaces.
        '''

        text = re.sub( '^\n+',    '',   text )
        text = re.sub( '\n+$',    '',   text )
        text = re.sub( '\n\s*\n', '\n', text )
        return text

    # strips lines wich contain only HTML comments and whitespaces
    @staticmethod
    def remove_html_comments( html ):
        '''
        Strips HTML style comments ( <!--...--> ).
        '''

        return re.sub( '[\n\s]*<!--.*-->[\s\n]*', '', html )

    @staticmethod
    def remove_newlines( text, repl = '\n', line_length = 0 ):
        '''
        Removes new line characters from input.
        If "line_length" is set, tries to preserve desired length replacing newlines with the value of "repl".
        '''

        text = ScriptFormater.remove_empty_lines( text )

        if line_length == 0:
            return text
        else:
            cur_len = 0
            def newline_length_replacer( match ):
                if ( cur_len + ( match.end( 'content' ) - match.start( 'content' ) +1 ) <= line_length ):
                    cur_len += match.end( 'content' ) - match.start( 'content' ) +1
                    return ' ' + match.group( 'content' )
                else:
                    cur_len = match.end( 'content' ) - match.start( 'content' )
                    return repl + match.group( 'content' )
            return ScriptFormater._NEWLINES_RE.sub( newline_length_replacer, text )

    @staticmethod
    def remove_spaces( text, repl = ' ' ):
        '''
        Removes multiple spaces and replaces them with value of "repl".
        '''

        return ScriptFormater._SPACES_RE.sub( repl, text )

    @staticmethod
    def trim_lines( text ):

        trim_re = re.compile( ScriptFormater._TRIM_PAT % re.escape( '\n' ), re.VERBOSE | re.MULTILINE )
        return trim_re.sub( ScriptFormater._trim_chars_replacer, text )

    @staticmethod
    def trim_chars( text, chars_pattern, is_html = False ):
        '''
        Remove spaces from around "chars_pattern" specified characters.
        HTML spaces work otherwise than script, set "is_html" argument.
        '''

        if ( is_html ):
            trim_re = re.compile( ScriptFormater._TRIM_PAT_HTML % re.escape( chars_pattern ), re.VERBOSE | re.MULTILINE )
        else:
            trim_re = re.compile( ScriptFormater._TRIM_PAT % re.escape( chars_pattern ), re.VERBOSE | re.MULTILINE )
        return trim_re.sub( ScriptFormater._trim_chars_replacer, text )

    @staticmethod
    def remove_spaces_outside_quotes( text, is_html = False ):
        '''
        Removes multiple spaces from "text" preserving those inside quotes.
        HTML spaces work otherwise than script, set "is_html" argument.
        '''

        if ( is_html ):
            return ScriptFormater._SPACES_OUTSIDE_QUOTES_RE_HTML.sub( ScriptFormater._spaces_outside_quotes_replacer, text )
        else:
            return ScriptFormater._SPACES_OUTSIDE_QUOTES_RE.sub( ScriptFormater._spaces_outside_quotes_replacer, text )

    @staticmethod
    def remove_comments( text ):
        '''
        Removes single- and multiline comments from text. Comment formats are as follows:
        #1: Anything between "/*" and "*/"
        #2: Anything between "//" and newline character
        '''

        return ScriptFormater._COMMENT_RE.sub( ScriptFormater._comment_replacer, text )

    @staticmethod
    def remove_c_style_comments( text ):
        '''
        Removes C style comments from text.
        '''

        return ''.join( [
            match.group( 'noncomment' )
            for match in ScriptFormater._C_STYLE_COMMENT_RE.finditer( text )
                if match.group( 'noncomment' )
        ] )

    # TODO
    #@staticmethod
    #def replace_quotes_escaped( text, to_replace = '"' )

    #@staticmethod
    #def HTML_list_tags( html ):
        #'''
        #WIP
        #'''

        #print '---------------------------\n-> Searching for HTML tags\n---------------------------\n'

        #for match in ScriptFormater._HTML_TAG_RE.finditer( html ):
            #print 'Found: ' + repr( match.group( ) ) + ' @' + repr( match.span( ) )
            #print '    tagname:    ' + repr( match.group( 'tagname' ) )
            #print '    tagclass:   ' + repr( match.group( 'tagclass' ) )
            #print '    attributes: ' + repr( ScriptFormater.trim_lines( ScriptFormater.remove_spaces_outside_quotes( ScriptFormater.remove_newlines( match.group( 'attributes' ), ' ' ) ) ) )
            #print '    closing:    ' + repr( match.group( 'closing' ) is '/' )
            #print '    selfclosed: ' + repr( match.group( 'selfclosed' ) is '/' ) + '\n'

    #@staticmethod
    #def strip( script, extension ):
        #'''
        #WIP
        #'''

        #script = ScriptFormater.trim_lines( script )

        #if ( extension == FrontendSettings.HTML ):
            #script = ScriptFormater.remove_html_comments( script )
        #else:
            #script = ScriptFormater.remove_comments( script )

        #script = ScriptFormater.remove_spaces_outside_quotes( script, extension == FrontendSettings.HTML )
        #script = ScriptFormater.remove_newlines( script, '\n', FrontendSettings.COMPRESS_WIDTH )

        #if ( extension == FrontendSettings.HTML ):
            #script = ScriptFormater.trim_chars( script, '<>/', True )
        #elif ( extension == FrontendSettings.CSS ):
            #script = ScriptFormater.trim_chars( script, ';{}:' )
        #else:
            #script = ScriptFormater.trim_chars( script, ';,[](){}=+-*/%!?:<>' )

        #return script

    #--------------------------
    # PRIVATE STATIC FUNCTIONS
    #--------------------------

    @staticmethod
    def _spaces_outside_quotes_replacer( match ):
        '''
        Private replacer function for "re.sub( )".
        '''

        def g( st ):
            return match.group( st )

        if g( 'spaces' ) is not None:
            return ' '
        else:
            return g( 'nonspace' )

    @staticmethod
    def _trim_chars_replacer( match ):
        '''
        Private replacer function for "re.sub( )".
        '''

        def g( st ):
            return match.group( st )

        if g( 'char' ) is not None:
            return g( 'char' )
        else:
            return g( 'nonchar' )

    @staticmethod
    def _comment_replacer( match ):
        '''
        Private replacer function for "re.sub( )".
        '''

        def g( st ):
            return match.group( st )

        if g( 'singlecomment' ):
            return ''
        elif g( 'multicomment' ):
            if ( g( 'linestart' ) is None ) or  ( g( 'lineend' ) is None ):
                return '\n'
            if ( g( 'linestart' ) is not None ) and ( g( 'lineend' ) is not None ):
                return ''
        elif g( 'noncomment' ):
            ret = g( 'noncomment' )
            if g( 'before' ):
                ret = ' ' + ret
            if g( 'after' ):
                ret = ret + ' '
            return ret
