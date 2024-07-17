from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QGridLayout


class ResponsiveWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout principal vertical
        main_layout = QVBoxLayout()

        # Layout horizontal para o topo
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Label 1"))
        top_layout.addWidget(QPushButton("Button 1"))

        # Layout de grade para o meio
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Label 2"), 0, 0)
        grid_layout.addWidget(QPushButton("Button 2"), 0, 1)
        grid_layout.addWidget(QLabel("Label 3"), 1, 0)
        grid_layout.addWidget(QPushButton("Button 3"), 1, 1)

        # Adicionar layouts ao layout principal
        main_layout.addLayout(top_layout)
        main_layout.addLayout(grid_layout)

        # Definir o layout principal na janela
        self.setLayout(main_layout)

        self.setWindowTitle("Responsive PyQt6 Application")
        self.show()


app = QApplication([])
window = ResponsiveWindow()
app.exec()
