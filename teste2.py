import time
# import os
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QMessageBox,
)
from hti_funcoes import criar_tabelas, conexao_banco
import hti_global as hg
# from menu import criar_menu

app = QApplication([])
# app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\siscom.ui")
# icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
# tela.setWindowIcon(icon)
# tela.setWindowTitle(f"ACESSO AO SISTEMA         {hg.SISTEMA}  Versao: {hg.VERSAO}")
# # Centraliza a janela na tela
# qt_rectangle = tela.frameGeometry()
# center_point = app.primaryScreen().availableGeometry().center()
# qt_rectangle.moveCenter(center_point)
# tela.move(qt_rectangle.topLeft())
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_login = QIcon(f"{hg.c_imagem}\\login.png")

conexao_banco()


# def verificar_senha():
#     index = tela.comboBox.currentIndex()
#     mop = tela.comboBox.itemText(index)
#     mcod_op = mop[0:3]
#     entry_senha_editado = str(tela.inp_senha.text().upper().strip())
#
#     start_time = time.time()
#     hg.conexao_cursor.execute(
#         f"SELECT * FROM insopera WHERE scod_op = '{mcod_op}' AND plug = '{entry_senha_editado}'"
#     )
#     arq_senha = hg.conexao_cursor.fetchone()
#     hg.conexao_bd.commit()
#     print(f"Tempo para verificar senha: {time.time() - start_time} segundos")
#
#     if arq_senha is not None:
#         hg.geral_cod_usuario = arq_senha[0]
#         hg.geral_nivel_usuario = arq_senha[12]
#         tela.close()
#         criar_menu()
#     else:
#         QMessageBox.warning(tela, "Erro de login", "SENHA INCORRETA!")
#         tela.inp_senha.clear()
#         tela.inp_senha.setFocus()


def fecha_tela():
    tela.close()
    hg.conexao_cursor.close()
    hg.conexao_bd.close()
    app.quit()


def siscom():
    # start_time = time.time()
    if hg.mtipo_temrinal == "S":
        criar_tabelas()

    hg.conexao_cursor.execute("SELECT scod_op, snome FROM insopera")
    arq_insopera = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()

    for ret_insopera in arq_insopera:
        item = f"{ret_insopera[0]} - {ret_insopera[1]}".strip("(),")
        tela.comboBox.addItem(item)
    # # tela.inp_senha.setReadOnly(False)
    # # tela.inp_senha.returnPressed.connect(verificar_senha)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_login.setIcon(icon_login)

    # tela.bt_login.clicked.connect(verificar_senha)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.show()
    # print(f"Tempo para carregar dados de login: {time.time() - start_time} segundos")
    # app.exec()


if __name__ == "__main__":
    start_time = time.time()
    siscom()
    print(f"Tempo para carregar inicio: {time.time() - start_time} segundos")
    app.exec()
    tela.close()
    hg.conexao_cursor.close()
    hg.conexao_bd.close()
    app.quit()
