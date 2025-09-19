# Mengimport componen dari Qt
import sys
import os
import re

from PySide6 import QtWidgets, QtCore, QtGui
# import library as library

# UI
class LauncherApps(QtWidgets.QMainWindow):
        # TODO : Buat function pemisah
        # 1. buat function untuk memisahkan antara
        # a. UI
        # b. Event
        # c. private properties
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

    # layout apps content
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
        
        layout_content = QtWidgets.QHBoxLayout()
        layout_content.addWidget(self.panel_button)
        layout_content.addWidget(self.panel_info)

        content_widget = QtWidgets.QWidget()
        content_widget.setLayout(layout_content)
        content_widget.setFixedSize(1200, 800)

        # apps content combine with search bar
        layout_content_vertical = QtWidgets.QVBoxLayout()
        layout_content_vertical.addWidget(self.panel_search)
        layout_content_vertical.addWidget(content_widget)

        right_side_content = QtWidgets.QWidget()
        right_side_content.setLayout(layout_content_vertical)
        right_side_content.setFixedSize(1200, 850)

        # Final layout
        all_layout_result = QtWidgets.QHBoxLayout()
        all_layout_result.addWidget(self.panel_list)
        all_layout_result.addWidget(right_side_content)

        result = QtWidgets.QWidget()
        result.setLayout(all_layout_result)
        result.setFixedSize(1500, 900)
    
        self.setCentralWidget(result)

    # menampung sinyal
    def _signal_container(self):
        # Dari sumber ke target sinyal
        self.panel_list.path_selected.connect(self.panel_button.create_button)
        self.panel_button.list_transfer.connect(self.panel_info.create_widget_from_list_detail)
        self.panel_search.search_text_signal.connect(self.panel_button.get_signal_from_search)

# List Department
class DepartmentList(QtWidgets.QWidget):
    path_selected = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self._ui_setup()

    def _ui_setup(self):
        list_department = QtWidgets.QListWidget()
        list_department.setFixedSize(290, 850)

        self.list_dir = self.get_dir_path()
        list_department.addItems(self.list_dir)
        list_department.itemClicked.connect(self.get_list_dir_name)

        list_layout = QtWidgets.QVBoxLayout()
        list_layout.addWidget(list_department)

        self.setLayout(list_layout)

    def get_dir_path(self):
        # TODO buat jadi funciton sendiri
        self.root_dir = "launcher_app\lmn_tools"
        self.list_dir = []
        for item_name in os.listdir(self.root_dir):
            temp_dir = os.path.join(self.root_dir, item_name)
            if os.path.isdir(temp_dir):
                self.list_dir.append(item_name)
        return self.list_dir
    
    def get_list_dir_name(self, item):
        self.item_text = item.text()
        print(f"get_list_dir_name = {self.item_text}")
        self.path_department = os.path.join(self.root_dir,
                                            self.item_text)
        print(f"emmit{self.path_department}")
        self.path_selected.emit(self.path_department)

# Button apps
class ButtonAppsHolder(QtWidgets.QWidget):
    list_transfer = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui_setup()

    def _ui_setup(self):
        self.root_dir = None
        self.grid = QtWidgets.QGridLayout()
        self.grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop |
                               QtCore.Qt.AlignmentFlag.AlignLeft)
        self.grid.setContentsMargins(10, 10, 10, 10)
        # Membuat container untuk button yang sudah di buat
        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.setExclusive(True)

        self.setLayout(self.grid)

    # TODO
    # hapus unused function
    def update_root_dir(self, path):
        self.root_dir = path
        
        print(f"selected dir : {self.root_dir}")
        self.cleanup_button()

        self.get_list_dir = []
        # output ['AdvancedRenamer', 'PureRef', 'ReNamer', 'ScreenToGif', 'UpdateCinesync', 'VideoToGif']
        
        # TODO
        # jangan pakai native variable
        # eg: dir, type, list
        for name_dir in os.listdir(self.root_dir):
            full_path = os.path.join(self.root_dir, name_dir)
            if os.path.isdir(full_path):
                self.get_list_dir.append(name_dir)
        
        self.get_specific_file()

        return self.get_list_dir

    # TODO : ini untuk apa?
    # get path file function
    def get_specific_file(self):
        self.get_file_png_list = []
        self.get_file_txt_list = []
        self.get_file_lnk_list = []

        for extention_file in os.listdir(self.root_dir):
            # mendapatkan path directoriy
            full_path = os.path.join(self.root_dir, extention_file)
            print(full_path)
            png_found = None        
            txt_found = None       
            lnk_found = None       
            if os.path.isdir(full_path):
                for a in os.listdir(full_path):
                    b = os.path.join(full_path, a)
                    # print(b)
                    if os.path.isfile(b):
                        if b.endswith(".png"):
                            png_found = b      
                        elif b.endswith(".txt"):
                            txt_found = b
                        elif b.endswith(".lnk"):
                            lnk_found = b

            if png_found:
                # jika terdapat nilai path maka akan di append
                self.get_file_png_list.append(png_found)
            else:
                # jika tidak akan mengirim string kosong
                self.get_file_png_list.append(None)

            if txt_found:
                # jika terdapat nilai path maka akan di append
                self.get_file_txt_list.append(txt_found)
            else:
                # jika tidak akan mengirim string kosong
                self.get_file_txt_list.append(None)

            if lnk_found:
                # jika terdapat nilai path maka akan di append
                self.get_file_lnk_list.append(lnk_found)
            else:
                # jika tidak akan mengirim string kosong
                self.get_file_lnk_list.append(None)

    # To get positions coloumb coordinate
    def get_grid_coordinate(self):
        self.positions = []
        for row in range(5):
            for col in range(3):
                self.positions.append((row, col))
        return self.positions
    
    # Merubah title case bersambung menambahkan space sebelum uppercase letter di button
    def fixed_title_letter(self,get_dir):
        display_text = ''
        for text, word in enumerate(get_dir):
            if word.isupper() and text != 0:
                display_text += ' ' + word
            else:
                display_text += word
        return display_text
    
    # TODO
    # buat function dengan tujuan create_button
    def create_button(self,path_address):
        self.positions = self.get_grid_coordinate()
        self.get_list_dir = self.update_root_dir(path_address)
        # button properties
        # TODO buat jadi function sendiri
        for positions, get_dir, get_png, get_txt, get_lnk in zip(self.positions,
                                                                 self.get_list_dir,
                                                                 self.get_file_png_list,
                                                                 self.get_file_txt_list,
                                                                 self.get_file_lnk_list):
            data_list_each_button = [get_dir, get_png, get_txt, get_lnk]

            title_fixed = self.fixed_title_letter(get_dir)

            button = QtWidgets.QPushButton(icon=QtGui.QIcon(get_png),
                                           text=title_fixed)

            button.setFixedSize(200, 100)
            button.setCheckable(True)
            button.setProperty("button_data", data_list_each_button)
            button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                 QtWidgets.QSizePolicy.Fixed)
            button.clicked.connect(self.slot_data_button_checked)
            button.setContentsMargins(10, 10, 10, 10)
            self.button_group.addButton(button)
            self.grid.addWidget(button, *positions, alignment=(QtCore.Qt.AlignmentFlag.AlignTop |
                                                               QtCore.Qt.AlignmentFlag.AlignLeft))

    def cleanup_button(self):
        for item in reversed(range(0, self.grid.count())):
            widget = self.grid.itemAt(item).widget()
            if widget:
                widget.setParent(None)

    def slot_data_button_checked(self):
        get_list_data_button = self.sender().property("button_data")
        print(f"emit from slot_data_button_checked= {get_list_data_button}")
        self.list_transfer.emit(get_list_data_button)

        for button in self.button_group.buttons():
            if button.isChecked():
                print(f"Button {button.text()} is checked")

    # TODO cari tahu logic search yang benar pada text
    def get_signal_from_search(self, text_search):
        for button in self.button_group.buttons():
            self.got_button_text = button.text()
            if text_search.strip() == "":
                button.show()
            # elif self.got_button_text.lower() == text_search.strip().lower():
            #     button.show()
            elif re.search(text_search.lower(),self.got_button_text.lower()):
                button.show()
            else:
                button.hide()

# Info Panel
class InfoSidePanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._ui_setup()

    def _ui_setup(self):
        # Layout
        self.info_layout = QtWidgets.QVBoxLayout()

        self.setLayout(self.info_layout)
        self.setFixedSize(450, 800)

    # TODO hapus function yang berlebih
    
    def create_widget_from_list_detail(self, list_details):
        # Urutan data list yang di dapat [get_dir,get_png,get_txt,get_lnk]
        list_button_details = list_details
        self.title_list = list_button_details[0]
        self.icon_list = list_button_details[1]
        self.description_list = list_button_details[2]
        self.shortcut_list = list_button_details[3]
        
        self.delete_layout_information()

        # Merubah title case bersambung menambahkan space sebelum uppercase letter di title
        # TODO buat jadi function (menggunakan function yang sudah ada)
        display_text = ButtonAppsHolder.fixed_title_letter(self, self.title_list)

        # Label Judul Applikasi widget
        self.title_apps = QtWidgets.QLabel(display_text)
        self.title_apps.setFixedSize(450, 50)

        # Label Icon applikasi widget
        self.icon_apps = QtWidgets.QLabel()
        self.icon_apps.setFixedSize(450, 200)
        self.icon_apps.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Error handling ketika tidak ditemukan file image nya
        if self.icon_list:
            self.icon_apps.setPixmap(QtGui.QPixmap(self.icon_list).scaled(100, 100))
        elif self.icon_list is None:
            self.icon_apps.setPixmap(QtGui.QPixmap(r"launcher_app\icon\owl.png").scaled(100, 100))

        # Information widget
        self.apps_description = QtWidgets.QPlainTextEdit()
        self.apps_description.setFixedSize(450, 300)
     
        # Error handling ketika tidak ditemukan file description nya
        # TODO: perbaiki penulisan logic
        if self.description_list:
            file = open(self.description_list, mode="r")
            self.apps_description.insertPlainText(file.read())
        elif self.description_list is None:
            self.apps_description.insertPlainText("There is no description here")

        # Button Run
        run_button = QtWidgets.QPushButton("RUN")
        run_button.setFixedSize(450, 50)
        run_button.clicked.connect(self.run_button_clicked)

        self.info_layout.addWidget(self.title_apps)
        self.info_layout.addWidget(self.icon_apps)
        self.info_layout.addWidget(self.apps_description)
        self.info_layout.addWidget(run_button)

    def run_button_clicked(self):
        os.startfile(self.shortcut_list)

    def delete_layout_information(self):
        for item in reversed(range(0, self.info_layout.count())):
            widget_item = self.info_layout.itemAt(item)
            if widget_item is not None:
                widget = widget_item.widget()
                if widget is not None:
                    widget.setParent(None)

# Search Bar
class EditText(QtWidgets.QWidget):
    search_text_signal = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self._ui_setup()
    
    def _ui_setup(self):
        self.text_bar = QtWidgets.QLineEdit()
        self.text_bar.setPlaceholderText("Search Here")
        self.text_bar.setFixedSize(1130, 50)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.text_bar)
        self.setLayout(layout)

        self.text_bar.textChanged.connect(self.get_signal_text)

    def get_signal_text(self, text):
        self.search_text_signal.emit(text)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout_all_component()

    def project_list_text_signal(self, text):
        print(text)
        self.folder_selected = text

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

        tree_model = QtGui.QStandardItemModel()
        root_node_name = tree_model.invisibleRootItem()
        # ---------------------------------------------
        

        root_directory_path_project = "batch-file"

        if os.path.exists(root_directory_path_project):
            self.tree_folder(root_node_name,root_directory_path_project)
        # ---------------------------------------------
        project_folder.setModel(tree_model)
        project_folder.clicked.connect(self.get_value)

        # layout setting
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(project_list)
        vertical_layout.addWidget(project_folder)

        # Grouping Project Dropdown menu and Folder Tree

        # self.setLayout()
        group_box.setLayout(vertical_layout)

        self.setCentralWidget(group_box)

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

def main():
    # seperti pembungkus dari semua program untuk di jalankan programnya
    app = QtWidgets.QApplication(sys.argv)

    # Membuat window
    window = LauncherApps()
    window.show()

    # memulai event loop
    app.exec()

if __name__ == "__main__":
    main()
