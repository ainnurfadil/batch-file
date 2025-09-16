import bpy

from qtpy import QtWidgets

from Acacia.lib.decoration import decor_acacia

from . import menu_main


class BlenderHostLMN(object):
    NAME = "Blender_LMN"

    def __init__(self):
        super(BlenderHostLMN, self).__init__()

    @decor_acacia
    def install(self):
        self.install_menu_main()

    def uninstall(self):
        self.uninstall_menu_main()

    def install_menu_main(self):
        menu_main.register()

    def uninstall_menu_main(self):
        menu_main.unregister()
