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
        .L                                       
        
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
        button_generate.clicked.connect(self.process_selected_objects)

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
        selected_objects = cmds.ls(selection=True)
        if not selected_objects:
            cmds.warning("Please select at least one object.")
            return False

        for obj in selected_objects:
            # Get the shaders connected to the object
            shaders = cmds.listConnections(obj, type='shadingEngine')
            if shaders:
                # Check if lambert1 is among the connected shaders
                if 'initialShadingGroup' in shaders:
                    return True  # Object is connected to lambert1
        return False  # Object is not connected to lambert1

    def disconnect_lambert1(self, obj):
        """Disconnects lambert1 from the given object."""
        try:
            # Get all shading groups connected to the object
            shading_groups = cmds.listConnections(obj, type='shadingEngine')

            if shading_groups and 'initialShadingGroup' in shading_groups:
                # Disconnect the object from lambert1
                cmds.disconnectShadingEngine(obj, 'initialShadingGroup')
                print(f"Disconnected {obj} from lambert1")
        except Exception as e:
            print(f"Error disconnecting {obj} from lambert1: {e}")

    def assign_proxy_material(self, obj, material_name):
        """
        Assign proxy material for selected object
        """
        # Assign new material proxy
        try:
            cmds.hyperShade(assign=material_name, o=obj)  # Use the object directly
            print(f"Assigned {material_name} to {obj}")
        except Exception as e:
            print(f"Error assigning material to {obj}: {e}")

    def check_list_object(self):
        """
        Check the object are available in the outliner (Error handling).
        """

    def delete_naming_object_selected(self):
        """
        Reload name object selected
        """

    def make_SG_and_material(self, object_selected):
        """Make proxy material and shading group."""

        # Make material nodes
        material_nodes = cmds.shadingNode('lambert', name=f"{object_selected}Proxy", asShader=True)

        # Make shading group nodes
        shading_group_nodes = cmds.sets(name=f"{object_selected}Proxy_SG", empty=True, renderable=True, noSurfaceShader=True)

        # Connect material and shading group
        cmds.connectAttr(material_nodes + ".outColor", shading_group_nodes + ".surfaceShader")

        return f"{object_selected}Proxy" # Return the material name

    def disconnect_initial_material(self):
        """
        Generate material
        """
        # Select inital material
        # cmds.select("lambert1")  # No need to select

        # Disconnect initial material connection
        try:
            cmds.disconnectAttr( 'lambert1.outColor','initialShadingGroup.surfaceShader' )
            cmds.disconnectAttr( 'lambert1.outColor','initialParticleSE.surfaceShader' )
            print("Disconnected lambert1 from initialShadingGroup and initialParticleSE")
        except Exception as e:
            print(f"Error disconnecting lambert1: {e}")

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

    def process_selected_objects(self):
        """
        Process all selected objects: disconnect lambert1 if connected and assign proxy material.
        """
        selected_objects = cmds.ls(selection=True, fullPath=True)

        if not selected_objects:
            cmds.warning("Please select at least one object.")
            return

        all_objects = []
        for obj in selected_objects:
            all_objects.append(obj)
            all_objects.extend(self.get_all_children(obj))

        self.disconnect_initial_material()

        for obj in all_objects:
            # Check and disconnect lambert1
            shaders = cmds.listConnections(obj, type='shadingEngine')
            if shaders and 'initialShadingGroup' in shaders:
                self.disconnect_lambert1(obj)

            # Make proxy material and assign it
            material_name = self.make_SG_and_material(cmds.listRelatives(obj, parent=True)[0] if cmds.listRelatives(obj, parent=True) else obj)  # Pass object name without full path
            self.assign_proxy_material(obj, material_name)

def show():
    QtAcacia.run(TexturingTools, host="maya")

if __name__ == '__main__':
    show()


    def process_selected_objects(self):
        """
        Process selected objects:
        1. List all objects in the scene, including children of the selected object.
        2. Check if each object is connected to the initial material (lambert1) and disconnect it.
        3. Assign a new proxy material to each object.
        """
        selected_objects = cmds.ls(selection=True, long=True)  # Get selected objects with full paths
        if not selected_objects:
            QtWidgets.QMessageBox.warning(self, "Warning", "No object selected!")
            return

        # Get all children of the selected objects
        all_objects = cmds.listRelatives(selected_objects, allDescendents=True, fullPath=True) or []
        all_objects.extend(selected_objects)  # Include the selected objects themselves

        # Process each object
        for obj in all_objects:
            # Check if the object is connected to lambert1
            shading_groups = cmds.listConnections(obj, type="shadingEngine") or []
            for sg in shading_groups:
                connected_material = cmds.listConnections(f"{sg}.surfaceShader", source=True) or []
                if "lambert1" in connected_material:
                    # Disconnect lambert1 from the shading group
                    cmds.disconnectAttr("lambert1.outColor", f"{sg}.surfaceShader")
                    print(f"Disconnected lambert1 from {obj}")

            # Assign a new proxy material
            proxy_material = self.create_proxy_material(obj)
            cmds.select(obj)
            cmds.hyperShade(assign=proxy_material)
            print(f"Assigned proxy material '{proxy_material}' to {obj}")

    def create_proxy_material(self, object_name):
        """
        Create a proxy material and shading group for the given object.
        Returns the name of the proxy material.
        """
        # Create a new lambert material
        material_name = f"{object_name}_Proxy"
        shading_group_name = f"{material_name}_SG"

        if not cmds.objExists(material_name):
            material_name = cmds.shadingNode("lambert", name=material_name, asShader=True)
            shading_group_name = cmds.sets(name=shading_group_name, empty=True, renderable=True, noSurfaceShader=True)
            cmds.connectAttr(f"{material_name}.outColor", f"{shading_group_name}.surfaceShader")

        return material_name

# ...existing code...

    def check_object_shader(self):
        """
        Trigger the process_selected_objects method when the button is clicked.
        """
        self.process_selected_objects()


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
        print("clicked")
        object_selected = cmds.ls(selection=True)

        if object_selected:
            self.choose_object_list =  object_selected[0]
        else:
            self.choose_object_list =  str("")

        print(f"panel history = {self.choose_object_list}")
        
        self.selected_object_name.setText(f"{self.choose_object_list}")

        self.status_layout.addWidget(self.selected_object_label)
        self.status_layout.addWidget(self.selected_object_name)
        self.status_layout.addWidget(self.edit_button)
        return self.choose_object_list

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
            if node == "shadingEngine":
                cmds.disconnectAttr(f'{select_lambert1}.outColor',f'{node}.surfaceShader')
    
    def make_shadingEngine_and_material_node(self):
        """
        Make proxy shading engine node and proxy material lambert based node
        """
        object_selection = cmds.ls(selection=True)

        object_list_pointing = object_selection[0]

        # make material nodes
        material_nodes = cmds.shadingNode('lambert', name=f"{object_list_pointing}Proxy", asShader=True)

        # make shading group nodes
        shading_group_nodes = cmds.sets(name=f"{object_list_pointing}Proxy_SG", empty=True, renderable=True, noSurfaceShader=True)

        #connect material and shading group
        cmds.connectAttr(material_nodes + ".outColor", shading_group_nodes + ".surfaceShader")

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


    def assign_proxy_material(self):
        """
        Assign proxy material for selected object
        """
        # Select object
        cmds.select("bola")

        # Assign new material proxy
        cmds.hyperShade(assign="bolaProxy")

        # Assign new material proxy
        try:
            cmds.hyperShade(assign=material_name, o=obj)  # Use the object directly
            print(f"Assigned {material_name} to {obj}")
        except Exception as e:
            print(f"Error assigning material to {obj}: {e}")

    def check_list_object(self):
        """
        Check the object are available in the outliner (Error handling).
        """

    def delete_naming_object_selected(self):
        """
        Reload name object selected
        """


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

    def process_selected_objects(self):
        """
        Process all selected objects: disconnect lambert1 if connected and assign proxy material.
        """
        selected_objects = cmds.ls(selection=True, fullPath=True)

        if not selected_objects:
            cmds.warning("Please select at least one object.")
            return

        all_objects = []
        for obj in selected_objects:
            all_objects.append(obj)
            all_objects.extend(self.get_all_children(obj))

        self.disconnect_initial_material()

        for obj in all_objects:
            # Check and disconnect lambert1
            shaders = cmds.listConnections(obj, type='shadingEngine')
            if shaders and 'initialShadingGroup' in shaders:
                self.disconnect_lambert1(obj)

            # Make proxy material and assign it
            material_name = self.make_SG_and_material(cmds.listRelatives(obj, parent=True)[0] if cmds.listRelatives(obj, parent=True) else obj)  # Pass object name without full path
            self.assign_proxy_material(obj, material_name)

def show():
    QtAcacia.run(TexturingTools, host="maya")

if __name__ == '__main__':
    show()
