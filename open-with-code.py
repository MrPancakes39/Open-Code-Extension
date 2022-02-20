# "Open with Code" extension is made by Salman Hasan
#  based on open-terminal.py example by Martin Enlund

import os

from gi.repository import Caja, GObject


class OpenCodeExtension(Caja.MenuProvider, GObject.GObject):
    def __init__(self):
        pass

    def _open_code(self, file, isDir):
        filename = file.get_location().get_path()
        os.chdir(filename)

        if isDir:
            os.system("code . &")
        else:
            os.system("code %s &" % filename)

    def menu_activate_cb(self, menu, file):
        self._open_code(file, False)

    def menu_background_activate_cb(self, menu, file):
        self._open_code(file, True)

    def get_file_items(self, window, files):
        if len(files) != 1:
            return

        file = files[0]
        if not file.is_directory() or file.get_uri_scheme() != "file":
            return

        item = Caja.MenuItem(name="CajaPython::opencode_file_item",
                             label="Open with Code",
                             tip="Open Code In %s" % file.get_name(),
                             icon="code")
        item.connect("activate", self.menu_activate_cb, file)
        return [item]

    def get_background_items(self, window, file):
        item = Caja.MenuItem(name="CajaPython::opencode_item",
                             label="Open with Code",
                             tip="Open Code In This Directory",
                             icon="code")
        item.connect("activate", self.menu_background_activate_cb, file)
        return [item]
