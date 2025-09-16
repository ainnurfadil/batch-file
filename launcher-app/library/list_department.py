from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QPushButton, QListWidgetItem
from PySide6.QtCore import Signal
import sys
import os

class DepartmentList(QWidget):
    pathSelected = Signal(str)
    def __init__(self):
        super().__init__()

        self.listDepartment = QListWidget()

        rootDir = "C:\workspace\learning\launcher_app\lmn_tools"

        self.getListDir = [f for f in os.listdir(rootDir) if os.path.isdir(os.path.join(rootDir, f))]
        
        # for item in self.getListDir:
        self.listDepartment.addItems(self.getListDir)
            # self.buttonCLicked = self.listDepartment.itemClicked(self.get_list_dir_name)
            
        self.listDepartment.itemClicked.connect(self.get_list_dir_name)
        
        # self.signal = QListWidgetItem(self.getsignal)
        # self.signal.text()

        listLayout = QVBoxLayout()
        listLayout.addWidget(self.listDepartment)

        # self

        self.setLayout(listLayout)

    def get_list_dir_name(self,item):
        self.getText = item.text()
        self.getPathDepartment = os.path.join(".\\lmn_tools\\",self.getText)
        # print(self.getPathDepartment)
        self.pathSelected.emit(self.getPathDepartment)
    
    # def main(self):
    #     self.getDataPath = self.getPathDepartment
    #     return self.getDataPath
    
    @staticmethod
    def example():
        return DepartmentList.main() 
    
    # def selected_item(self):

        
if __name__ == "__main__":
    app = QApplication(sys.argv)        # seperti pembungkus dari semua program untuk di jalankan programnya
    # Membuat window
    window = DepartmentList()
    window.show()
    # memulai event loop
    app.exec()

