import os

from qtpy import QtWidgets,QtGui

from Acacia.tools import QtAcacia

from maya import cmds, mel

ICONS_DIR = os.path.join(os.getenv("ACACIA"),"resources/Images/toolsIcon/maya")

class TexturingTools(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TexturingTools, self).__init__(parent=parent)
        self.init_ui()

    def init_ui(self):
        """
        Make UI
        """
        # Layout setting
        self.status_layout = QtWidgets.QHBoxLayout()
        general_layout = QtWidgets.QVBoxLayout()

        # Widget status selected object name
        self.selected_object_label = QtWidgets.QLabel(f"Object Selected \t:")
        self.edit_button = QtWidgets.QPushButton()
        self.selected_object_name = QtWidgets.QLineEdit()

        # Push button edit_button
        icon_edit_path = (os.path.join(ICONS_DIR,"general/publish/Edit.png"))
        self.edit_button.setIcon(QtGui.QIcon(icon_edit_path))
        self.edit_button.clicked.connect(self.get_active_object_name)

        self.get_active_object_name()

        status_widget_convert = QtWidgets.QWidget()
        status_widget_convert.setLayout(self.status_layout)

        button_generate = QtWidgets.QPushButton("Generate Proxy Material")
        button_generate.clicked.connect(self.check_object_shader)

        general_layout.addWidget(status_widget_convert)
        general_layout.addWidget(button_generate)

        result = QtWidgets.QWidget()
        result.setLayout(general_layout)

        self.setCentralWidget(result)


    def get_active_object_name(self):
        """
        Get name object selected. Output string.
        """
        print("clicked")
        object_selected = cmds.ls(selection=True)

        if object_selected:
            choose_object_list =  object_selected[0]
        else:
            choose_object_list =  str("")

        print(f"panel history = {choose_object_list}")
        
        self.selected_object_name.setText(f"{choose_object_list}")

        self.status_layout.addWidget(self.selected_object_label)
        self.status_layout.addWidget(self.selected_object_name)
        self.status_layout.addWidget(self.edit_button)
        return choose_object_list

    def check_object_shader(self):
        """
        Check if object assigned default shader (lambert1)
        """

    def disconnect_initial_material(self):
        """
        Generate material
        """
        # Select inital material
        cmds.select("lambert1")

        # Disconenct initial material connection
        cmds.disconnectAttr( 'lambert1.outColor','initialShadingGroup.surfaceShader' )
        cmds.disconnectAttr( 'lambert1.outColor','initialParticleSE.surfaceShader' )

    def assign_proxy_material(self):
        """
        Assign proxy material for selected object
        """
        # Select object
        cmds.select("bola")

        # Assign new material proxy
        cmds.hyperShade(assign="bolaProxy")

    def check_list_object(self):
        """
        Check the object are available in the outliner (Error handling).
        """

    def delete_naming_object_selected(self):
        """
        Reload name object selected
        """
        
    def make_SG_and_material(self):
        a = cmds.ls(selection=True)

        object_selected = a[0]

        # make material nodes
        material_nodes = cmds.shadingNode('lambert', name=f"{object_selected}Proxy", asShader=True)

        # make shading group nodes
        shading_group_nodes = cmds.sets(name=f"{object_selected}Proxy_SG", empty=True, renderable=True, noSurfaceShader=True)

        #connect material and shading group
        cmds.connectAttr(material_nodes + ".outColor", shading_group_nodes + ".surfaceShader")


def show():
    QtAcacia.run(TexturingTools, host="maya")

if __name__ == '__main__':
    show()