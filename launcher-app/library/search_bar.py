from PySide6.QtWidgets import QWidget, QLineEdit, QApplication,QHBoxLayout
import sys

class EditText(QWidget):
    def __init__(self):
        super().__init__()
        textBar = QLineEdit("Search Here")
        textBar.setFixedSize(500,50)

        layout = QHBoxLayout()

        layout.addWidget(textBar)

        self.setLayout(layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)        # seperti pembungkus dari semua program untuk di jalankan programnya
    # Membuat window
    window = EditText()
    window.show()
    # memulai event loop
    app.exec()