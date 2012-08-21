# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#---------
# IMPORTS
#---------

# global
import sys
import os
import time
import atexit
from signal import SIGTERM 

#-------------
# UNIX DAEMON
#-------------

class UnixDaemon( object ):
    '''
    A generic daemon class.
    Usage: subclass the Daemon class and override the run( ) method.
    '''

    if ( hasattr( os, 'devnull' ) ):
        REDIRECT_TO = os.devnull
    else:
        REDIRECT_TO = '/dev/null'

    def __init__( self, pidfile, killparentproc = False, stdin = REDIRECT_TO, stdout = REDIRECT_TO, stderr = REDIRECT_TO ):
        '''
        Constructor.
        '''

        self.killparentproc = killparentproc
        self.stdin          = stdin
        self.stdout         = stdout
        self.stderr         = stderr
        self.pidfile        = pidfile

    def daemonize( self ):
        '''
        Do the UNIX double-fork magic, see Stevens' "Advanced Programming in the UNIX Environment" for details
        (ISBN 0201563177) http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        '''

        try: 
            pid = os.fork( )
            if ( pid > 0 ):
                # exit first parent
                if ( self.killparentproc ):
                    sys.exit( 0 )
                else:
                    return
        except OSError, e:
            sys.stderr.write( 'Fork #1 failed: %d (%s)\n' % ( e.errno, e.strerror ) )
            sys.exit( 1 )

        # decouple from parent environment
        os.chdir( '/' )
        os.setsid( )
        os.umask( 0 )

        # do second fork
        try: 
            pid2 = os.fork( )
            if pid2 > 0:
                # exit from second parent
                sys.exit( 0 )
        except OSError, e:
            sys.stderr.write( 'Fork #2 failed: %d (%s)\n' % ( e.errno, e.strerror ) )
            sys.exit( 1 )

        # redirect standard file descriptors
        sys.stdout.flush( )
        sys.stderr.flush( )
        si = file( self.stdin, 'r' )
        so = file( self.stdout, 'a+' )
        se = file( self.stderr, 'a+', 0 )
        os.dup2( si.fileno( ), sys.stdin.fileno( ) )
        os.dup2( so.fileno( ), sys.stdout.fileno( ) )
        os.dup2( se.fileno( ), sys.stderr.fileno( ) )

        # write pidfile
        atexit.register( self.delpid )
        pid = str( os.getpid( ) )
        file( self.pidfile, 'w+' ).write( '%s\n' % pid )

        return pid

    def delpid( self ):
        '''
        Deletes the pid file.
        '''

        if os.path.exists( self.pidfile ):
            os.remove( self.pidfile )

    def start( self ):
        '''
        Start the daemon.
        '''

        # Check for a pidfile to see if the daemon already runs
        try:
            pf  = file( self.pidfile, 'r' )
            pid = int( pf.read( ).strip( ) )
            pf.close( )
        except IOError:
            pid = None

        if pid:
            message = 'Pidfile %s already exist. Daemon already running?\n' % self.pidfile
            sys.stderr.write( message )
            sys.exit( 1 )

        # Start the daemon
        if ( self.daemonize( ) > 0 ):
            self.run( )

    def stop( self ):
        '''
        Stop the daemon.
        '''

        # Get the pid from the pidfile
        try:
            pf  = file( self.pidfile, 'r' )
            pid = int( pf.read( ).strip( ) )
            pf.close( )
        except IOError:
            pid = None

        if not pid:
            message = 'Pidfile %s does not exist. Daemon not running?\n' % self.pidfile
            sys.stderr.write( message )
            return # not an error in a restart

        # Try killing the daemon process    
        try:
            while 1:
                os.kill( pid, SIGTERM )
                time.sleep( 0.1 )
        except OSError, err:
            err = str( err )
            if err.find( 'No such process' ) > 0:
                self.delpid( )
            else:
                print( str( err ) )
                sys.exit( 1 )

    def restart( self ):
        '''
        Restart the daemon.
        '''

        self.stop( )
        self.start( )

    def run( self ):
        '''
        This function will be called after the process has been daemonized by start( ) or restart( ).
        Must be overridden, raises RuntimeError otherwise.
        '''

        raise RuntimeError( 'UnixDaemon::run( ) must be overridden!' )
