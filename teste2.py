from PyQt6.QtWidgets import QApplication, QRadioButton, QVBoxLayout, QWidget, QButtonGroup

if __name__ == '__main__':
    app = QApplication([])
    widget = QWidget()
    layout = QVBoxLayout(widget)

    rb1 = QRadioButton("Opção 1")
    rb2 = QRadioButton("Opção 2")
    r3 = QRadioButton("Atacado")
    r4 = QRadioButton("Varejo")

    group1 = QButtonGroup()
    group1.addButton(rb1)
    group1.addButton(rb2)

    group2 = QButtonGroup()
    group2.addButton(r3)
    group2.addButton(r4)

    layout.addWidget(rb1)
    layout.addWidget(rb2)
    layout.addWidget(r3)
    layout.addWidget(r4)

    widget.show()
    app.exec()
