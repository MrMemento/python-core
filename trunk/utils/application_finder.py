# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#---------
# IMPORTS
#---------

# global
import os
import re
import fnmatch

# custom
from core.constants.sys_constants import SysConstants as SC

#--------------------
# APPLICATION FINDER
#--------------------

class ApplicationFinder( object ):
    '''
    Class for finding installed applications on diferent platforms.
    '''

    #------------------
    # STATIC VARIABLES
    #------------------

    SUPPORTED_OPERATING_SYSTEMS = [
        SC.UNIX,
        SC.WINDOWS,
        SC.OSX,
    ]

    _DPKG_LIST_PROGRAMS_COMMAND  = 'dpkg --get-selections \'%s\''
    _DPKG_SPLIT_PROGRAMS_PATTERN = '\s+(?:de)?install\n'
    _DPKG_LIST_FILES_COMMAND     = 'dpkg -L \'%s\''
    _DPKG_SPLIT_FILES_PATTERN    = '\n'

    _RPM_LIST_PROGRAMS_COMMAND  = 'rpm -qa \'%s\''
    _RPM_SPLIT_PROGRAMS_PATTERN = '\n'
    _RPM_LIST_FILES_COMMAND     = 'rpm -ql \'%s\''
    _RPM_SPLIT_FILES_PATTERN    = '\n'

    _SYSTEM_PROFILER_LIST_PROGRAMS_COMMAND = 'system_profiler SPApplicationsDataType'
    _SYSTEM_PROFILER_APPLICATION_PATTERN   = '   %s:'
    _SYSTEM_PROFILER_APPLICATION_INFO      = '      '
    _SYSTEM_PROFILER_INSTALL_LOCATION      = '      Location: '

    _WINREG_UNINSTALL_KEY    = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\'
    _WINREG_DISPLAY_NAME     = 'DisplayName'
    _WINREG_INSTALL_LOCATION = 'InstallLocation'
    

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self, operating_system, indent = 0 ):
        '''
        Constructor.
        Raises error if OS is not supported.
        '''

        if not operating_system in ApplicationFinder.SUPPORTED_OPERATING_SYSTEMS:
            raise RuntimeError( 'Application finding is not supported on operating system: "%s" Please extend the module, or restrict list of supported operating systems!' % operating_system )

        self.indent           = indent
        self.operating_system = operating_system

    #------------------
    # PUBLIC FUNCTIONS
    #------------------

    def find_applications_by_pattern( self, pattern, executable ):
        '''
        Function for finding installed applications based on given name pattern and executable RegExp string.
        '''

        return {
            SC.UNIX:    self._find_unix_binaries,
            SC.WINDOWS: self._find_windows_binaries,
            SC.OSX:     self._find_osx_binaries,
        }[ self.operating_system ]( pattern, executable )

    def find_binaries_walk( self, directories, executable ):
        '''
        Function for finding given binary by pattern "executable" in list of "directories".
        '''

        #-----------------------------
        # inner loop function - start
        #-----------------------------

        def _find_in_possible_binaries( path, possible_binaries, executable, found_binaries ):

            for possible_binary in possible_binaries:
                if executable.match( possible_binary ):
                    found_binaries.append( os.path.join( path, possible_binary ) )
                    return

        #---------------------------
        # inner loop function - end
        #---------------------------

        executable     = re.compile( executable )
        found_binaries = [ ]

        # for every found program directory
        for install_directory in directories:
            # for every file in the found program directory's tree hierarchy
            for path, subdirectories, possible_binaries in os.walk( install_directory ):
                _find_in_possible_binaries( path, possible_binaries, executable, found_binaries )

        return found_binaries

    #----------------------
    # PRIVATE UNIX METHODS
    #----------------------

    def _find_unix_binaries( self, pattern, executable ):
        '''Function for finding applications on Unix platform.'''

        # try debian systems
        try:
            return self._find_dpkg_binaries( pattern, executable )
        except Exception, e:
            #print e
            pass

        # try redhat systems
        try:
            return self._find_rpm_binaries( pattern, executable )
        except Exception, e:
            #print e
            pass

        return False

    def _find_dpkg_binaries( self, pattern, executable ):
        '''Find binaries based on DPKG information.'''

        return self._find_binaries_shell(
            pattern, executable,
            ApplicationFinder._DPKG_LIST_PROGRAMS_COMMAND, ApplicationFinder._DPKG_SPLIT_PROGRAMS_PATTERN,
            ApplicationFinder._DPKG_LIST_FILES_COMMAND, ApplicationFinder._DPKG_SPLIT_FILES_PATTERN
        )

    def _find_rpm_binaries( self, pattern, executable ):
        '''Find binaries based on DPKG information.'''

        return self._find_binaries_shell(
            pattern, executable,
            ApplicationFinder._RPM_LIST_PROGRAMS_COMMAND, ApplicationFinder._RPM_SPLIT_PROGRAMS_PATTERN,
            ApplicationFinder._RPM_LIST_FILES_COMMAND, ApplicationFinder._RPM_SPLIT_FILES_PATTERN
        )

    def _find_binaries_shell(
        self,
        pattern, executable,
        programs_command, programs_separator,
        files_command, files_separator,
    ):
        '''Collected code for finding packages based on RPM or DPKG information'''

        import subprocess

        return_output = subprocess.check_output(
            programs_command % pattern,
            shell  = True,
            stderr = subprocess.STDOUT
        )

        separator        = re.compile( programs_separator )
        application_list = separator.split( return_output )
        if len( application_list ) > 0 and application_list[ -1 ] is '':
            application_list = application_list[ 0 : -1 ]

        binaries   = [ ]
        separator  = re.compile( files_separator )
        executable = re.compile( executable )

        # for each matching application
        for application in application_list:

            # find all files in package
            return_output = subprocess.check_output(
                files_command % application,
                shell  = True,
                stderr = subprocess.STDOUT
            )
            possible_executable_list = separator.split( return_output )
            if len( possible_executable_list ) > 0 and possible_executable_list[ -1 ] is '':
                possible_executable_list = possible_executable_list[ 0 : -1 ]

            # for each file in matching application
            for possible_executable in possible_executable_list:

                # check if matches executable pattern and not present
                if executable.search( possible_executable ) and possible_executable not in binaries:
                    binaries.append( possible_executable )

        return binaries

    #---------------------
    # PRIVATE OSX METHODS
    #---------------------

    def _find_osx_binaries( self, pattern, executable ):
        '''Function for finding applications on OSX platform.'''

        # try debian systems
        try:
            return self._find_system_profiler_binaries( pattern, executable )
        except Exception, e:
            print e
            pass

        return False

    def _find_system_profiler_binaries( self, pattern, executable ):
        '''Lists applications based on system_profiler.'''

        import subprocess

        return_output = subprocess.check_output(
            ApplicationFinder._SYSTEM_PROFILER_LIST_PROGRAMS_COMMAND,
            shell  = True,
            stderr = subprocess.STDOUT
        ).split( '\n' )

        pattern             = re.compile( fnmatch.translate( ApplicationFinder._SYSTEM_PROFILER_APPLICATION_PATTERN % pattern ), re.IGNORECASE )
        install_directories = [ ]
        exclude_lines       = [ ]
        for index, line in enumerate( return_output ):

            if index not in exclude_lines and pattern.match( line ):

                # omit empty line following line containing application name
                exclude_lines.append( index +1 )
                i = index +2

                while return_output[ i ].startswith( ApplicationFinder._SYSTEM_PROFILER_APPLICATION_INFO ):

                    # append application info line to excluded lines
                    exclude_lines.append( i )
                    # check if info line is install location
                    if return_output[ i ].startswith( ApplicationFinder._SYSTEM_PROFILER_INSTALL_LOCATION ):
                        install_directories.append( return_output[ i ][ len( ApplicationFinder._SYSTEM_PROFILER_INSTALL_LOCATION ) : ] )
                    # increment line number
                    i += 1

        return self.find_binaries_walk( install_directories, executable )

    #-------------------------
    # PRIVATE WINDOWS METHODS
    #-------------------------

    def _find_windows_binaries( self, pattern, executable ):
        '''Function for finding applications on Windows platform.'''

        # try _winreg registry values
        try:
            return self._find_registry_binaries( pattern, executable )
        except Exception, e:
            #print e
            pass

        return False

    def _find_registry_binaries( self, pattern, executable ):
        '''Lists applications based on registry entries.'''

        from core.utils.registry_walker import RegistryWalkwer

        #--------------------------
        # recursive parser - start
        #--------------------------

        def _find_in_registry_entries( entries, name_re ):

            results = [ ]
            for key in entries:

                if entries[ key ].has_key( ApplicationFinder._WINREG_DISPLAY_NAME ) and \
                    entries[ key ].has_key( ApplicationFinder._WINREG_INSTALL_LOCATION ) and \
                    name_re.match( entries[ key ][ ApplicationFinder._WINREG_DISPLAY_NAME ] ) and \
                    not entries[ key ][ ApplicationFinder._WINREG_INSTALL_LOCATION ] in results:
                        results.append( 
                            entries[ key ][ ApplicationFinder._WINREG_INSTALL_LOCATION ]
                        )

                if entries[ key ].has_key( RegistryWalkwer.SUBKEYS ):
                    results.extend(
                        _find_in_registry_entries( entries[ key ][ RegistryWalkwer.SUBKEYS ], pattern )
                    )

            return results

        #------------------------
        # recursive parser - end
        #------------------------

        entry_patterns = (
            ApplicationFinder._WINREG_DISPLAY_NAME,
            ApplicationFinder._WINREG_INSTALL_LOCATION,
        )

        registry_entries = RegistryWalkwer.build_object(
            RegistryWalkwer.HKEY_LOCAL_MACHINE,
            ApplicationFinder._WINREG_UNINSTALL_KEY,
            entry_patterns
        )[ RegistryWalkwer.SUBKEYS ]

        translated_pattern  = re.compile( fnmatch.translate( pattern ), re.IGNORECASE )
        install_directories = _find_in_registry_entries( registry_entries, translated_pattern )

        return self.find_binaries_walk( install_directories, executable )
