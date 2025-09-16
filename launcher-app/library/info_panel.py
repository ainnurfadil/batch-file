from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QPlainTextEdit, QVBoxLayout, QPushButton  # Mengimport componen dari Qt
import sys

class InfoSidePanel(QWidget):
    def __init__(self):
        super().__init__()
        # Label Judul Applikasi
        titleApps = QLabel("Apps 1")
        titleApps.setFixedSize(500,50)

        # Label Icon applikasi
        iconApps = QLabel()
        iconApps.setFixedSize(500,500)
        iconApps.setPixmap(QPixmap("icon\owl.png"))

        # Information Window
        appsDescription = QPlainTextEdit()
        appsDescription.setFixedSize(500,50)
        appsDescription.insertPlainText("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus imperdiet tortor nec velit facilisis finibus. Quisque quis gravida leo, vitae blandit est. Suspendisse potenti. Duis mattis odio a turpis congue pharetra. Aliquam erat ex, tincidunt ut hendrerit a, vehicula scelerisque risus. Fusce fermentum mauris ac lacus mollis, et iaculis elit scelerisque. Mauris eu pharetra magna. Suspendisse vestibulum sagittis urna, ut suscipit ligula efficitur ut.")

        # Button Run
        runButton = QPushButton("RUN")
        runButton.setFixedSize(500,50)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(titleApps)
        layout.addWidget(iconApps)
        layout.addWidget(appsDescription)
        layout.addWidget(runButton)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)        # seperti pembungkus dari semua program untuk di jalankan programnya
    # Membuat window
    window = InfoSidePanel()
    window.show()
    # memulai event loop
    app.exec()