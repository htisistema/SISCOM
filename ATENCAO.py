from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
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
    return


def atencao(mensagem):
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    text_browser = tela.findChild(QtWidgets.QTextBrowser, "textBrowser")
    text_browser.setText(f"{mensagem}")

    tela.show()
    app.exec()


if __name__ == "__main__":
    atencao('teste ')
