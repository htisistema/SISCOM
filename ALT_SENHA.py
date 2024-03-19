# ALTERAR OPERADOR

import os

# import socket
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QMessageBox
from hti_funcoes import conexao_banco
from venda_pdv import executar_consulta
import hti_global as hg

# Crie a janela
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\alt_senha.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
tela.setWindowIcon(icon)
tela.setWindowTitle(f"MUDAR DE OPERADOR         {hg.SISTEMA}  Versao: {hg.VERSAO}")
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
icon_login = QIcon(f"{hg.c_imagem}\\login.png")

if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(180, 180)  # redimensiona a imagem para 100x100
tela.lb_imagem.setPixmap(pixmap_redimensionado)
conexao_banco()
mopcao = 0


def on_close_event(event):
    tela.close()
    event.accept()


tela.closeEvent = on_close_event


def verificar_senha():
    global mopcao
    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    mcod_op = mop[0:3]
    entry_senha_editado = str(tela.inp_senha.text().upper().strip())
    hg.conexao_cursor.execute(
        f"SELECT * FROM insopera WHERE scod_op = '{mcod_op}' "
        f"and plug = '{entry_senha_editado}'"
    )
    # Recupere o resultado
    arq_senha = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_senha is not None:
        hg.geral_cod_usuario = arq_senha[0]
        hg.geral_nivel_usuario = arq_senha[12]
        tela.close()
        if mopcao == 1:
            executar_consulta()

        return True
    else:
        QMessageBox.warning(tela, "Erro de login", "SENHA INCORRETA!")
        tela.inp_senha.clear()
        tela.inp_senha.setFocus()
        return False


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    hg.conexao_cursor.close()
    hg.conexao_bd.close()
    app.quit()


def dados_login(mop):
    global mopcao
    mopcao = mop
    # hg.conexao_cursor.execute("SELECT * FROM sacsetup")
    # # Recupere o resultado
    # m_set = hg.conexao_cursor.fetchall()
    # hg.conexao_bd.commit()

    # if hg.mtipo_temrinal == "S":
    #     criar_tabelas()
    hg.conexao_cursor.execute(f"SELECT scod_op,snome FROM insopera")
    arq_insopera = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()

    for ret_insopera in arq_insopera:
        item = f"{ret_insopera[0]} - {ret_insopera[1]}".strip("(),")
        tela.comboBox.addItem(item)
    tela.inp_senha.setReadOnly(False)
    tela.inp_senha.returnPressed.connect(verificar_senha)
    tela.bt_login.setIcon(icon_login)
    tela.bt_login.clicked.connect(verificar_senha)

    tela.show()
    app.exec()


if __name__ == "__main__":
    dados_login(1)
    # Feche a conexão
    tela.close()
    hg.conexao_cursor.close()
    hg.conexao_bd.close()
    app.quit()
