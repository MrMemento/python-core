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
import tkMessageBox
import tkFileDialog
import tkColorChooser

# common

#----------------
# DIALOG MANAGER
#----------------

class DialogManager:
    '''
    Static wrapper class for working with tkinter dialogs.
    '''

    ABORT  = tkMessageBox.ABORT
    RETRY  = tkMessageBox.RETRY
    IGNORE = tkMessageBox.IGNORE
    OK     = tkMessageBox.OK
    CANCEL = tkMessageBox.CANCEL
    YES    = tkMessageBox.YES
    NO     = tkMessageBox.NO

    #-----------------------
    # PUBLIC STATIC METHODS
    #-----------------------

    @staticmethod
    def show_info_dialog(
        master,
        dialog_title,
        dialog_message
    ):
        '''
        Show an info message dialog.
        "master": The tk instance that owns the dialog.
        "dialog_title": Title of the dialog.
        "dialog_message": Message to display in dialog.
        '''

        return tkMessageBox.showinfo(
            dialog_title, dialog_message,
            parent = master
        )

    @staticmethod
    def show_warning_dialog(
        master,
        dialog_title,
        dialog_message
    ):
        '''
        Show an info message dialog.
        "master": The tk instance that owns the dialog.
        "dialog_title": Title of the dialog.
        "dialog_message": Message to display in dialog.
        '''

        return tkMessageBox.showwarning(
            dialog_title, dialog_message,
            parent = master
        )

    @staticmethod
    def show_error_dialog(
        master,
        dialog_title,
        dialog_message
    ):
        '''
        Show an info message dialog.
        "master": The tk instance that owns the dialog.
        "dialog_title": Title of the dialog.
        "dialog_message": Message to display in dialog.
        '''

        return tkMessageBox.showerror(
            dialog_title, dialog_message,
            parent = master
        )

    @staticmethod
    def show_yes_no_dialog(
        master,
        dialog_title,
        dialog_message,
        default_button = None
    ):
        '''
        Show an info message dialog.
        "master": The tk instance that owns the dialog.
        "dialog_title": Title of the dialog.
        "dialog_message": Message to display in dialog.
        "default_button": Default button to be selected when dialog appears.
        '''

        return tkMessageBox.askyesno(
            dialog_title, dialog_message,
            parent  = master,
            default = default_button
        )

    @staticmethod
    def show_ok_cancel_dialog(
        master,
        dialog_title,
        dialog_message,
        default_button = None
    ):
        '''
        Show an info message dialog.
        "master": The tk instance that owns the dialog.
        "dialog_title": Title of the dialog.
        "dialog_message": Message to display in dialog.
        "default_button": Default button to be selected when dialog appears.
        '''

        return tkMessageBox.askokcancel(
            dialog_title, dialog_message,
            parent  = master,
            default = default_button
        )

    @staticmethod
    def show_retry_cancel_dialog(
        master,
        dialog_title,
        dialog_message,
        default_button = None
    ):
        '''
        Show an info message dialog.
        "master": The tk instance that owns the dialog.
        "dialog_title": Title of the dialog.
        "dialog_message": Message to display in dialog.
        "default_button": Default button to be selected when dialog appears.
        '''

        return tkMessageBox.askretrycancel(
            dialog_title, dialog_message,
            parent  = master,
            default = default_button
        )

    @staticmethod
    def show_file_open_dialog(
        master,
        dialog_title,
        file_types   = None,
        multiple     = False,
        initial_dir  = None,
        initial_file = None
    ):
        '''
        Show a file open dialog.
        "master": The tk instance that owns the dialog.
        "dialog_title": Title of the dialog.
        "file_types": List of touples containing (label, pattern). Example: [ ('PNG files', '.png'), ... ]
        "multiple": Is multiple file selection enabled. Default is False.
        "initial_dir": Initial directory string.
        "initial_file": Initial file name string.
        '''

        return tkFileDialog.askopenfilename(
            title       = dialog_title,
            parent      = master,
            multiple    = multiple,
            filetypes   = file_types,
            initialdir  = initial_dir,
            initialfile = initial_file
        )

    @staticmethod
    def show_directory_open_dialog(
        master,
        dialog_title,
        must_exist  = True,
        initial_dir = None
    ):
        '''
        Show a file open dialog.
        "master": The tk instance that owns the dialog.
        "dialog_title": Title of the dialog.
        "must_exist": Does the directory has to exist. Default is True
        "initial_dir": Initial directory string.
        '''

        return tkFileDialog.askdirectory(
            title      = dialog_title,
            parent     = master,
            mustexist  = must_exist,
            initialdir = initial_dir
        )

    @staticmethod
    def show_file_save_dialog(
        master,
        dialog_title,
        file_types        = None,
        default_extension = '',
        initial_dir       = None,
        initial_file      = None
    ):
        '''
        Show a file open dialog.
        "master": The tk instance that owns the dialog.
        "dialog_title": Title of the dialog.
        "file_types": List of touples containing (label, pattern). Example: [ ('PNG files', '.png'), ... ]
        "default_extension": Default extension string if user does not enter one.
        "initial_dir": Initial directory string.
        "initial_file": Initial file name string.
        '''

        return tkFileDialog.asksaveasfilename(
            title            = dialog_title,
            parent           = master,
            defaultextension = default_extension,
            filetypes        = file_types,
            initialdir       = initial_dir,
            initialfile      = initial_file
        )

    @staticmethod
    def show_color_dialog(
        master,
        dialog_title,
        dialog_color_tuple_or_hexa,
        request_tuple = True
    ):
        '''
        Show a color chooser dialog.
        "master": The tk instance that owns the dialog.
        "dialog_title": Title of the dialog.
        "dialog_color": Initial color string of the dialog, can be (R,G,B) tuple or hexa string.
        "request_tuple": If True, an (R,G,B) tuple is returned, else a hexa string. Default is True.
        '''

        # Returns ( None, None ) when user hits Cancel.
        rgb_tuple, hexa_string = tkColorChooser.askColor(
            dialog_color_tuple_or_hexa,
            title  = dialog_title,
            parent = master
        )

        if hexa_string is None:
            return False
        elif request_tuple:
            return rgb_tuple
        else:
            return hexa_string

    #-------------
    # CONSTRUCTOR
    #-------------

    def __init__( self ):
        '''
        Static constructor.
        Raises Exception.
        '''

        raise RuntimeError( 'Tried to instantiate static class!' )
