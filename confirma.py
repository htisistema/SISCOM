from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
import os
import hti_global as hg

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\hti_confirmacao.ui")
tela.setWindowTitle("CONFIRMACAO")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela.empresa.setPixmap(pixmap_redimensionado)


def fecha_tela():
    tela.close()


def confirma_sim():
    fecha_tela()
    print("True")
    return True


def confirma_nao():
    fecha_tela()
    print("False")
    return False


mop1 = ""


def confirma(mop, mensagem):
    global mop1
    mop1 = mop
    tela.bt_nao.setIcon(icon_sair)
    text_browser = tela.findChild(QtWidgets.QTextBrowser, "textBrowser")
    text_browser.setText(f"{mensagem}")
    if mop == "S":
        tela.bt_sim.setFocus()
    else:
        tela.bt_nao.setFocus()

    tela.bt_nao.clicked.connect(confirma_nao)
    tela.bt_sim.clicked.connect(confirma_sim)
    tela.show()


def keyPressEvent(event):
    if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
        if mop1 == "S":
            confirma_sim()
        else:
            confirma_nao()
    elif event.key() == Qt.Key.Key_Escape:
        confirma_nao()


tela.keyPressEvent = keyPressEvent

if __name__ == "__main__":
    mopcao = (confirma("S", "teste "))
    print(mopcao)
    if mopcao:
        print("sim")
    else:
        print("nao")
    app.exec()
