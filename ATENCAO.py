from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
import os
import hti_global as hg

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\hti_atencao.ui")
tela.setWindowTitle("ATENCAO")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela.empresa.setPixmap(pixmap_redimensionado)


def fecha_tela():
    tela.close()


def atencao(mensagem):
    tela.bt_sair.setIcon(icon_sair)
    text_browser = tela.findChild(QtWidgets.QTextBrowser, "textBrowser")
    text_browser.setText(f"{mensagem}")
    tela.bt_sair.setFocus()
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.show()


def keyPressEvent(event):
    if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
        # print("Enter pressionado")
        fecha_tela()
    elif event.key() == Qt.Key.Key_Escape:
        # print("Esc pressionado")
        fecha_tela()


tela.keyPressEvent = keyPressEvent

if __name__ == "__main__":
    atencao("teste ")
    app.exec()
