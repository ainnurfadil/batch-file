import sys
import os

from PySide6 import QtWidgets, QtCore, QtGui

class FolderItem(QtGui.QStandardItem):
    def __init__(self, txt='', font_size=10, font_bold=False, font_color=QtGui.QColor(255,255,255)):
        super().__init__()
        font_style = QtGui.QFont("Segoe UI", font_size)
        font_style.setBold(font_bold)
        self.setIcon(QtGui.QIcon(r"launcher-app\icon\folder.png"))
        self.setEditable(False)
        self.setForeground(font_color)
        self.setFont(font_style)
        self.setText(txt)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_folder = QtWidgets.QTreeView()
        self.tree_model = QtGui.QStandardItemModel()
        self.project_folder.setModel(self.tree_model)
        self.project_folder.setHeaderHidden(True)
        self.project_folder.clicked.connect(self.get_value)
        self.project_name = self.get_list_folder_project()
        self.layout_all_component()

    def get_list_folder_project(self):
        project_dir = "batch-file"
        # Only list directories (projects)
        return [name for name in os.listdir(project_dir) if os.path.isdir(os.path.join(project_dir, name))]

    def tree_folder(self, parent_item, folder_path):
        for entry in os.scandir(folder_path):
            if entry.is_dir():
                item = FolderItem(entry.name)
                parent_item.appendRow(item)
                self.tree_folder(item, entry.path)

    def update_project_folder_tree(self, project_name):
        self.tree_model.clear()
        root_node = self.tree_model.invisibleRootItem()
        root_directory_path_project = os.path.join("batch-file", project_name)
        if os.path.exists(root_directory_path_project) and os.path.isdir(root_directory_path_project):
            root_item = FolderItem(project_name)
            root_node.appendRow(root_item)
            self.tree_folder(root_item, root_directory_path_project)
        self.project_folder.expandAll()

    def get_value(self, index):
        item = self.tree_model.itemFromIndex(index)
        print(item.text())

    def layout_all_component(self):
        group_box = QtWidgets.QGroupBox("Project")
        project_list = QtWidgets.QComboBox()
        project_list.addItems(self.project_name)
        project_list.currentTextChanged.connect(self.update_project_folder_tree)
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(project_list)
        vertical_layout.addWidget(self.project_folder)
        group_box.setLayout(vertical_layout)
        self.setCentralWidget(group_box)
        # Show initial tree for the first project
        if self.project_name:
            self.update_project_folder_tree(self.project_name[0])

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()





# ...existing code...

class ProjectTreePanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_folder = QtWidgets.QTreeView()
        self.tree_model = QtGui.QStandardItemModel()
        self.project_folder.setModel(self.tree_model)
        self.project_folder.setHeaderHidden(True)
        self.project_folder.clicked.connect(self.get_value)
        self.project_name = self.get_list_folder_project()

        self.project_list = QtWidgets.QComboBox()
        self.project_list.addItems(self.project_name)
        self.project_list.currentTextChanged.connect(self.update_project_folder_tree)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.project_list)
        layout.addWidget(self.project_folder)
        self.setLayout(layout)

        # Show initial tree for the first project
        if self.project_name:
            self.update_project_folder_tree(self.project_name[0])

    def get_list_folder_project(self):
        project_dir = "batch-file"
        return [name for name in os.listdir(project_dir) if os.path.isdir(os.path.join(project_dir, name))]

    def tree_folder(self, parent_item, folder_path):
        for entry in os.scandir(folder_path):
            if entry.is_dir():
                item = FolderItem(entry.name)
                parent_item.appendRow(item)
                self.tree_folder(item, entry.path)

    def update_project_folder_tree(self, project_name):
        self.tree_model.clear()
        root_node = self.tree_model.invisibleRootItem()
        root_directory_path_project = os.path.join("batch-file", project_name)
        if os.path.exists(root_directory_path_project) and os.path.isdir(root_directory_path_project):
            root_item = FolderItem(project_name)
            root_node.appendRow(root_item)
            self.tree_folder(root_item, root_directory_path_project)
        self.project_folder.expandAll()

    def get_value(self, index):
        item = self.tree_model.itemFromIndex(index)
        print(item.text())

# ...existing code...

class LauncherApps(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__private_properties()
        self._ui_setup()
        self._signal_container()

    def __private_properties(self):
        self.panel_button = ButtonAppsHolder()
        self.panel_info = InfoSidePanel()
        self.panel_list = DepartmentList()
        self.panel_search = EditText()
        self.panel_project_tree = ProjectTreePanel()  # Add this

    def _ui_setup(self):
        self.setWindowTitle("Apps Launcher")
        self.setFixedSize(1500, 900)

        self.panel_button.setFixedSize(700, 800)
        self.panel_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                        QtWidgets.QSizePolicy.Fixed)
        self.panel_info.setFixedSize(500, 800)
        self.panel_info.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                      QtWidgets.QSizePolicy.Fixed)
        self.panel_list.setFixedSize(300, 900)
        self.panel_list.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                      QtWidgets.QSizePolicy.Fixed)
        self.panel_search.setFixedSize(1170, 60)
        self.panel_search.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                        QtWidgets.QSizePolicy.Fixed)
        self.panel_project_tree.setFixedSize(300, 900)  # Set size for new panel

        layout_content = QtWidgets.QHBoxLayout()
        layout_content.addWidget(self.panel_button)
        layout_content.addWidget(self.panel_info)

        content_widget = QtWidgets.QWidget()
        content_widget.setLayout(layout_content)
        content_widget.setFixedSize(1200, 800)

        layout_content_vertical = QtWidgets.QVBoxLayout()
        layout_content_vertical.addWidget(self.panel_search)
        layout_content_vertical.addWidget(content_widget)

        right_side_content = QtWidgets.QWidget()
        right_side_content.setLayout(layout_content_vertical)
        right_side_content.setFixedSize(1200, 850)

        # Final layout: department list, project tree panel, right side content
        all_layout_result = QtWidgets.QHBoxLayout()
        all_layout_result.addWidget(self.panel_list)
        all_layout_result.addWidget(self.panel_project_tree)  # Add project tree panel
        all_layout_result.addWidget(right_side_content)

        result = QtWidgets.QWidget()
        result.setLayout(all_layout_result)
        result.setFixedSize(1500, 900)

        self.setCentralWidget(result)

    # ...existing code...