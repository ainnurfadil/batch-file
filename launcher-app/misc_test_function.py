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
        self.tree_model = QtGui.QStandardItemModel()  # Tambahkan ini
        self.project_folder = QtWidgets.QTreeView()   # Tambahkan ini
        self.layout_all_component()
        # initial_project = self.project_name.currentText()
        # if initial_project:
        #     self.update_project_folder_tree(initial_project)

    def project_list_text_signal(self, text):
        print(text)
        self.folder_selected = text
        self.update_project_folder_tree(text)

    def get_list_folder_project(self):
        project_dir = f"batch-file"
        self.project_name = os.listdir(project_dir)
        
        return self.project_name

    def tree_folder(self,parent_item_name,child_item_path):
        '''
        In this function it will make tree structure based on given directory
        path address.
        '''
        for name_folder in os.scandir(child_item_path):
            if name_folder.is_dir():
                item = FolderItem(name_folder.name)
                parent_item_name.appendRow(item)
                self.tree_folder(item,name_folder.path)
# -----------------------------------------------------
    def update_project_folder_tree(self, project_name):
        '''
        This function will update the tree view based on the selected project name.
        '''
        self.tree_model.clear()
        root_node_name = self.tree_model.invisibleRootItem()
        
        root_directory_path_project = os.path.join("batch-file", project_name)

        if os.path.exists(root_directory_path_project) and os.path.isdir(root_directory_path_project):
            # Add the root project folder itself to the tree
            root_item = FolderItem(project_name)
            root_node_name.appendRow(root_item)
            # Populate its children
            self.tree_folder(root_item, root_directory_path_project)
        
        self.project_folder.expandAll()
# -------------------------------------------------------

    def get_value(self,val):
        ''' 
        This function will be storing data from list tree that clicked by user,
        and after that it will be outputing the string value that equal with the 
        list directory.
        '''
        print(val.data())
        # print(val.row())
        # print(val.colomn())

    def layout_all_component(self):
        # Interface Project menu drop down
        self.get_list_folder_project()
        group_box = QtWidgets.QGroupBox("Project")

        # Interface for the name of ongoing project list
        project_list = QtWidgets.QComboBox()
        project_list.addItems(self.project_name)
        project_list.currentTextChanged.connect(self.project_list_text_signal)

        # Interface for folder tree in every project

        project_folder = QtWidgets.QTreeView()
        project_folder.setHeaderHidden(True)

        self.tree_model = QtGui.QStandardItemModel()
        root_node_name = self.tree_model.invisibleRootItem()
        # # ---------------------------------------------
        # root_directory_path_project = "batch-file"

        # if os.path.exists(root_directory_path_project):
        #     self.tree_folder(root_node_name,root_directory_path_project)
        # # ---------------------------------------------
        project_folder.setModel(self.tree_model)
        project_folder.clicked.connect(self.get_value)

        # layout setting
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(project_list)
        vertical_layout.addWidget(self.project_folder)

        # Grouping Project Dropdown menu and Folder Tree

        # self.setLayout()
        group_box.setLayout(vertical_layout)

        self.setCentralWidget(group_box)
                

app = QtWidgets.QApplication(sys.argv)

# Membuat window
window = MainWindow()
window.show()

# memulai event loop
app.exec()



