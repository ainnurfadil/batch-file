# TODO : 
# 1. avoid create multiple shader if already connected with same name
# # 2. add prefix {m_} for material name 
# 3. change to pep8 style + 80/90 char limit
# 4. change icon logo get selected object
# 5. give windows name
# 6. remove unused variable
# 7. cleanup `format` usage : use legacy f-string .format()

import os

from qtpy import QtWidgets,QtGui

from Acacia.tools import QtAcacia

from maya import cmds, mel

ICONS_DIR = os.path.join(os.getenv("ACACIA"),"resources/Images/toolsIcon/maya")

class TexturingTools(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TexturingTools, self).__init__(parent=parent)
        self.init_ui()
        self.bind_event()

    def init_ui(self):
        """
        Make UI
        """
        # Layout setting
        status_layout = QtWidgets.QHBoxLayout()
        general_layout = QtWidgets.QVBoxLayout()

        # Widget status selected object name
        selected_object_label = QtWidgets.QLabel("Group\Object Selected \t:")
        edit_button = QtWidgets.QPushButton()
        selected_object_name = QtWidgets.QLineEdit()

        # Push button edit_button
        icon_edit_path = (os.path.join(ICONS_DIR,"general/publish/Edit.png"))
        edit_button.setIcon(QtGui.QIcon(icon_edit_path))
        

        status_widget_convert = QtWidgets.QWidget()
        status_widget_convert.setLayout(status_layout)

        button_generate = QtWidgets.QPushButton("Generate Proxy Material")
        
        general_layout.addWidget(status_widget_convert)
        general_layout.addWidget(button_generate)

        result = QtWidgets.QWidget()
        result.setLayout(general_layout)

        self.setCentralWidget(result)

        # Declare local variable into as class variable
        self.status_layout = status_layout
        self.selected_object_label = selected_object_label
        self.edit_button = edit_button
        self.selected_object_name = selected_object_name
        self.button_generate = button_generate
        self.get_active_object_name()

    def bind_event(self):
        self.edit_button.clicked.connect(self.get_active_object_name)
        self.button_generate.clicked.connect(self.process_generate_button)

    def get_active_object_name(self):
        """
        Get name object selected. Output string.
        """
        object_selected = cmds.ls(selection=True)

        if object_selected:
            self.choose_object_list =  object_selected[0]
        else:
            self.choose_object_list =  str("")

        print("Group\Object Selected = {}".format(self.choose_object_list))
        
        self.selected_object_name.setText(f"{self.choose_object_list}")

        self.status_layout.addWidget(self.selected_object_label)
        self.status_layout.addWidget(self.selected_object_name)
        self.status_layout.addWidget(self.edit_button)

    def disconnect_initial_material(self):
        """
        Disconnect initial material (lambert1) that connected to 
        initial Shading Engine (SG)
        """
        # Inital material
        initial_node_name = "lambert1"
        lambert1_connection = cmds.listConnections(initial_node_name)
        default_inital_material = "{}.outColor".format(initial_node_name)

        for node in lambert1_connection:
            node_type = cmds.nodeType(node)

            # Disconenct initial material connection shadingEngine
            if node_type == "shadingEngine":
                cmds.disconnectAttr(default_inital_material,"{}.surfaceShader".format(node))

        print("Initial material and shading engine disconnected")
    
    def make_shadingEngine_and_material_node(self,object_selection):
        """
        Make proxy shading engine node and proxy material lambert based node
        """
        pointing_object_selection = object_selection[0]

        # make material nodes
        material_nodes = cmds.shadingNode("lambert", 
                                          name="m_{}Proxy".format(pointing_object_selection), 
                                          asShader=True)
        # print(f'Material created = {material_nodes}')

        # make shading group nodes
        shading_group_nodes = cmds.sets(name="{}Proxy_SG".format(pointing_object_selection), 
                                        empty=True, 
                                        renderable=True, 
                                        noSurfaceShader=True)
        # print(f'Shading engine created = {shading_group_nodes}')

        # connect material and shading group
        cmds.connectAttr("{}.outColor".format(material_nodes), 
                         "{}.surfaceShader".format(shading_group_nodes))
        # print(f"material {material_nodes} connected with {shading_group_nodes}")

    def delete_unused_hypershade_node(self):
        """
        Keep hypershade node clean from unused node.
        """
        mel.eval('''
                 hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");
                 ''')
        # print("Unused Hypershade node deleted")

    def assign_proxy_material(self,object_name):
        """
        Assign proxy material for selected object
        """
        pointing_object_name = object_name[0]
        # Assign new material proxy
        cmds.select("{}".format(pointing_object_name))
        cmds.hyperShade(assign="{}Proxy".format(pointing_object_name))
        # print(f"Assign object {pointing_object_name} to {pointing_object_name}Proxy")

    def process_generate_button(self):
        """
        Process when generate button clicked
        """
        self.delete_unused_hypershade_node()
        self.disconnect_initial_material()

        name_selected_object = self.choose_object_list
        list_polygon_name = cmds.listRelatives(f"{name_selected_object}",
                                               allDescendents=True, 
                                               type=["mesh","nurbsSurface"])
        
        for polygon in list_polygon_name:
            name_shape = cmds.listRelatives(f"{polygon}",p=True)
            self.make_shadingEngine_and_material_node(name_shape)

            self.assign_proxy_material(name_shape)
        

def show():
    QtAcacia.run(TexturingTools, host="maya")

if __name__ == '__main__':
    show()
