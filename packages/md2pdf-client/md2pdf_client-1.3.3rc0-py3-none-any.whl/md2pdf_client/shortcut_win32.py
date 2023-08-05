#!/usr/bin/env python3
'''
md2pdf_client: A client application to render a Markdown file into a PDF via a
connection to an md2pdf server.
Copyright (C) 2019  Sean Lanigan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import os
import pythoncom
from win32com.shell import shell


def get_path(folder_id):
    return shell.SHGetFolderPath(0, folder_id, None, 0)


def get_home():
    return os.path.expanduser("~")


def get_desktop():
    return os.path.join(os.path.expanduser("~"), "Desktop")


# Taken from: https://github.com/mhammond/pywin32/blob/master/pywin32_postinstall.py
def create_shortcut(path, description, filename, arguments="", workdir="", iconpath="", iconindex=0):
    ilink = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None,
                                       pythoncom.CLSCTX_INPROC_SERVER,
                                       shell.IID_IShellLink)
    ilink.SetPath(path)
    ilink.SetDescription(description)
    if arguments:
        ilink.SetArguments(arguments)
    if workdir:
        ilink.SetWorkingDirectory(workdir)
    if iconpath or iconindex:
        ilink.SetIconLocation(iconpath, iconindex)
    ipf = ilink.QueryInterface(pythoncom.IID_IPersistFile)
    ipf.Save(filename, 0)


def create_md2pdf_startmenu():
    desktop_folder = get_desktop()
    home_folder = get_home()

    print("Creating shortcut in: {}".format(desktop_folder))
    shortcut_path = os.path.join(desktop_folder, "md2pdf Client.lnk")
    shortcut_description = "Convert Markdown documents into PDF"
    launch_target = "md2pdf-client"
    launch_args = "%1 %*"
    working_dir = home_folder
    
    create_shortcut(
        launch_target,
        shortcut_description,
        shortcut_path,
        launch_args,
        working_dir
    )


if __name__ == "__main__":
    create_md2pdf_startmenu()
