import sys
import os

from PySide6 import QtWidgets, QtCore, QtGui

class FolderItem(QtGui.QStandardItem):
    def __int__(self, txt='', font_size=12, font_bold=False, font_color=QtGui.QColor(0,0,0)):
        super().__init__()

        font_style = QtGui.QFont('Segoe UI', font_size)
        font_style.setBold(font_bold)

        self.setEditable(False)
        self.setForeground(font_color)
        self.setFont(font_style)
        self.setText(txt)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Interface for folder tree in every project
        project_folder = QtWidgets.QTreeView()
        project_folder.setHeaderHidden(True)

        tree_model = QtGui.QStandardItemModel()
        root_node = tree_model.invisibleRootItem()

        # ---------------------------------------------

        indonesia = FolderItem('Indonesia')
        
        jawa_timur = FolderItem('Jawa Timur')
        jawa_tengah = FolderItem('Jawa Tengah')

        surabaya = FolderItem('Surabaya')
        malang = FolderItem('Malang')

        indonesia.appendRows([jawa_timur,jawa_tengah])
        jawa_timur.appendRows([malang,surabaya])

        japan = FolderItem('Japan')

        tokyo = FolderItem('Tokyo')
        hokkaido = FolderItem('Hokkaido')

        japan.appendRow([tokyo,hokkaido])

        root_node.appendRow(indonesia)
        root_node.appendRow(japan)

        project_folder.setModel(tree_model)
        project_folder.expandAll()
        project_folder.clicked.connect(self.get_value)

        ## in tree view set act like table

        self.setCentralWidget(project_folder)


    def get_value(self,val):
        print(val.data())
        # print(val.row())
        # print(val.colomn())
                

app = QtWidgets.QApplication(sys.argv)

# Membuat window
window = MainWindow()
window.show()

# memulai event loop
app.exec()



