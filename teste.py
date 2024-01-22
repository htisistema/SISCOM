import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGroupBox, QLabel, QVBoxLayout

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt6 GroupBox'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        groupBox = QGroupBox("GroupBox Example")
        vbox = QVBoxLayout()

        label = QLabel("Conteúdo do GrupoBox")
        vbox.addWidget(label)

        groupBox.setLayout(vbox)

        vbox_main = QVBoxLayout()
        vbox_main.addWidget(groupBox)
        self.setLayout(vbox_main)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
