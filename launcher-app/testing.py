"""
Maya code progress exploration
"""

a = cmds.listRelatives("box_GRP")
# a = ['bola', 'pCylinder']
container_of_nodetype = []
for list_relative in a:
    b = cmds.nodeType(list_relative)
    container_of_nodetype.append(b)
    
if container_of_nodetype == "mesh":
    cmds.hyperShade(assign="lambert3", objects=a)
else:
    for a_selection in a:
        list_relatives_loop = cmds.listRelatives(a_selection)
        
        container_of_node_relative_loop = []
        for node in list_relatives_loop:
            b = cmds.nodeType(list_relative)
            
        if b = "mesh":
            cmds.hyperShade(assign="lambert3", objects=a_selection)



"""
Maya tools code progress
"""

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
        self.selected_object_label = QtWidgets.QLabel(f"Group\Object Selected \t:")
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
        object_selected = cmds.ls(selection=True)

        if object_selected:
            self.choose_object_list =  object_selected[0]
        else:
            self.choose_object_list =  str("")

        print(f"Group\Object Selected = {self.choose_object_list}")
        
        self.selected_object_name.setText(f"{self.choose_object_list}")

        self.status_layout.addWidget(self.selected_object_label)
        self.status_layout.addWidget(self.selected_object_name)
        self.status_layout.addWidget(self.edit_button)

    def disconnect_initial_material(self):
        """
        Disconnect initial material (lambert1) that connected to initial Shading Engine (SG)
        """
        # Select inital material
        select_lambert1 = cmds.select("lambert1")

        check_lambert1_connection = cmds.listConnections(select_lambert1)

        list_node_type_connections = []
        for node in check_lambert1_connection:
            node_type = cmds.nodeType(node)
            list_node_type_connections.append(node_type)

            # Disconenct initial material connection shadingEngine
            if node_type == "shadingEngine":
                cmds.disconnectAttr(f'{select_lambert1}.outColor',f'{node}.surfaceShader')

        print(check_lambert1_connection)
        print(list_node_type_connections)
    
    def make_shadingEngine_and_material_node(self,object_selection):
        """
        Make proxy shading engine node and proxy material lambert based node
        """
        # make material nodes
        self.material_nodes = cmds.shadingNode('lambert', name=f"{object_selection}Proxy", asShader=True)

        # make shading group nodes
        shading_group_nodes = cmds.sets(name=f"{object_selection}Proxy_SG", empty=True, renderable=True, noSurfaceShader=True)

        #connect material and shading group
        cmds.connectAttr(f"{self.material_nodes}.outColor", f"{shading_group_nodes}.surfaceShader")

    def check_object_shader(self):
        """
        Check if object assigned default shader (lambert1)
        """
        # self.choose_object_list = cmds.ls(selection=True)
        if not self.choose_object_list:
            cmds.warning("Please select at least one object.")
            return False

        for obj in self.choose_object_list:
            # Get the shaders connected to the object
            shaders = cmds.listConnections(obj, type='shadingEngine')
            if shaders:
                # Check if lambert1 is among the connected shaders
                if 'initialShadingGroup' in shaders:
                    return True
        return False  # Object is not connected to lambert1

    def assign_proxy_material(self,object_selection):
        """
        Assign proxy material for selected object
        """
        # Assign new material proxy
        cmds.hyperShade(assign=f"{self.material_nodes}",objects=f"{object_selection}")

    def get_all_children(self, obj):
        """
        Get all children of an object recursively.
        """
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []
        all_children = []
        for child in children:
            all_children.append(child)
            all_children.extend(self.get_all_children(child))  # Recursive call
        return all_children

    def process_generate_button(self):
        """
        Process when generate button clicked
        """
        name_selected_object = self.choose_object_list
        # need itteration of object listed
        
        self.disconnect_initial_material()
        self.make_shadingEngine_and_material_node(name_selected_object)

        self.assign_proxy_material()

def show():
    QtAcacia.run(TexturingTools, host="maya")

if __name__ == '__main__':
    show()
