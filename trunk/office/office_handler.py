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
from subprocess import Popen

# 3rd party
try:
    import uno
except:
    import platform
    raise RuntimeError( 'Prerequisite "LibreOffice UNO module" for Python (v%s) could not be imported, please ensure it is installed as a 3rd party module!' % platform.python_version( ) )

# custom

#----------------
# OFFICE HANDLER
#----------------

class OfficeHandler( object ):
    '''
    Class for working with LibreOffice.
    '''

    #---------------------------------------
    # AVAILABLE LIBREOFFICE STARTUP OPTIONS
    #---------------------------------------

    #'--headless',       # like invisible but no userinteraction at all
    #'--nologo',         # don't show startup screen
    #'--norestore',      # suppress restart/restore after fatal errors
    #'--nolockcheck',    # don't check for remote instances using the installation
    #'--nodefault',      # don't start with an empty document
    #'--minimized',      # keep startup bitmap minimized
    #'--invisible',      # no startup screen, no default document and no UI
    #'--quickstart',     # starts the quickstart service
    #'--help',           # show this message and exit
    #'--version',        # display the version information
    #'--writer',         # create new text document
    #'--calc',           # create new spreadsheet document
    #'--draw',           # create new drawing
    #'--impress',        # create new presentation
    #'--base',           # create new database
    #'--math',           # create new formula
    #'--global',         # create new global document
    #'--web',            # create new HTML document

    #-------------------------
    # PUBLIC STATIC VARIABLES
    #-------------------------

    BACKGROUND_PROCESS_ARGUMENTS = [
        '--headless',
        '--nologo',
        '--norestore',
        '--nolockcheck',
        '--nodefault',
    ]

    CONNECTION_ARGUMENT = '--accept=socket,host=%s,port=%s;urp;StarOffice.ComponentContext'

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self, binary_path ):
        '''
        Constructor
        '''

        self._binary  = binary_path
        self._process = None
        self._host    = None
        self._port    = None

    #----------------
    # PUBLIC METHODS
    #----------------

    # -> PROCESS MANAGEMENT

    def start_background_process( self, host, port ):
        '''
        Starts a LibreOffice background process.
        Raises RuntimeError, if a LibreOffice process is already started.
        '''

        if not self._process is None:
            raise RuntimeError( 'LibreOffice subprocess is already started!' )

        self._host    = host
        self._port    = port
        self._process = Popen(
            [
                self._binary,
                OfficeHandler.CONNECTION_ARGUMENT % ( self._host, self._port )
            ].extend( OfficeHandler.BACKGROUND_PROCESS_ARGUMENTS )
        )

    def stop_process( self ):
        '''
        Stops started LibreOffice process.
        Raises RuntimeError, if no LibreOffice is started.
        '''

        if self._process is None:
            raise RuntimeError( 'LibreOffice subprocess not yet started!' )

        self._process.kill( )
        self._process = None
        self._host    = None
        self._port    = None

    def get_pid( self ):
        '''
        Returns started process' PID, or None when no process is started.
        '''

        if self._process is None:
            return None
        else:
            return self._process.pid

    # -> CONNECTION MANAGEMENT

    def connect_to_process( self, timeout = 5 ):
        '''
        Estabilishes connection to started LibreOffice process.
        "timeout" is how many seconds to keep trying. (Maybe function needs to wait for subprocess starting.) Defaults to 5 seconds.
        '''

        pass
