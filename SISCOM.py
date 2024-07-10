import time
import os
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QMessageBox,
)
from hti_funcoes import criar_tabelas, conexao_banco
import hti_global as hg
from menu import criar_menu

start_time = time.time()

app = QApplication([])
print(
    f"Tempo para carregar a interface do usuário: {time.time() - start_time} segundos"
)
start_time = time.time()
# app.setStyleSheet(hg.style_sheet)
# Carregar interface do usuário
tela = uic.loadUi(f"{hg.c_ui}\\siscom.ui")

# Configurações iniciais da tela
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
tela.setWindowIcon(icon)
tela.setWindowTitle(f"LOGIN         {hg.SISTEMA}  Versao: {hg.VERSAO}")
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())

# Carregar ícones
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_login = QIcon(f"{hg.c_imagem}\\login.png")

# Carregar imagens
if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(180, 180)
tela.lb_imagem.setPixmap(pixmap_redimensionado)

logohti = QPixmap(f"{hg.c_imagem}\\logoHTI.png")
pixmap_redimensionado = logohti.scaled(150, 150)
tela.logohti.setStyleSheet(
    "background-color: rgb(190, 216, 255);border-width: 0px;border-radius: 0px;"
)
tela.logohti.setPixmap(pixmap_redimensionado)

# Configurar label de versão
lbl_nome_cliente = tela.findChild(QtWidgets.QLabel, "versao")
lbl_nome_cliente.setText(f"Versao: {hg.VERSAO}")
print(
    f"Tempo para carregar a app.setStyleSheet(hg.style_sheet): {time.time() - start_time} segundos"
)

start_time = time.time()
conexao_banco()
print(f"Tempo para conectar ao banco de dados: {time.time() - start_time} segundos")


# def on_close_event(event):
#     tela.close()
#     event.accept()
#     tela.closeEvent = on_close_event


def verificar_senha():
    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    mcod_op = mop[0:3]
    entry_senha_editado = str(tela.inp_senha.text().upper().strip())

    hg.conexao_cursor.execute(
        f"SELECT * FROM insopera WHERE scod_op = '{mcod_op}' AND plug = '{entry_senha_editado}'"
    )
    arq_senha = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()

    if arq_senha is not None:
        hg.geral_cod_usuario = arq_senha[0]
        hg.geral_nivel_usuario = arq_senha[12]
        tela.close()
        criar_menu()
    else:
        QMessageBox.warning(tela, "Erro de login", "SENHA INCORRETA!")
        tela.inp_senha.clear()
        tela.inp_senha.setFocus()


def fecha_tela():
   tela.close()
   # tela.closeEvent = on_close_event
   hg.conexao_cursor.close()
   hg.conexao_bd.close()
   app.quit()


def dados_login():
    if hg.mtipo_temrinal == "S":
        criar_tabelas()

    hg.conexao_cursor.execute("SELECT scod_op, snome FROM insopera")
    arq_insopera = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()

    for ret_insopera in arq_insopera:
        item = f"{ret_insopera[0]} - {ret_insopera[1]}".strip("(),")
        tela.comboBox.addItem(item)
    tela.inp_senha.setReadOnly(False)
    tela.inp_senha.returnPressed.connect(verificar_senha)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_login.setIcon(icon_login)

    tela.bt_login.clicked.connect(verificar_senha)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.show()
    # app.exec()


if __name__ == "__main__":
    start_time = time.time()
    dados_login()
    print(f"Tempo para carregar inicio: {time.time() - start_time} segundos")
    app.exec()
    tela.close()
    hg.conexao_cursor.close()
    hg.conexao_bd.close()
    app.quit()

# # PRINCIPAL
# import os
# from PyQt6 import uic, QtWidgets
# from PyQt6.QtGui import QPixmap, QIcon
# from PyQt6.QtWidgets import QMessageBox
# from hti_funcoes import criar_tabelas, conexao_banco
# import hti_global as hg
# from menu import criar_menu
#
# app = QtWidgets.QApplication([])
# app.setStyleSheet(hg.style_sheet)
# tela = uic.loadUi(f"{hg.c_ui}\\siscom.ui")
# icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
# tela.setWindowIcon(icon)
# tela.setWindowTitle(f"LOGIN         {hg.SISTEMA}  Versao: {hg.VERSAO}")
# # Centraliza a janela na tela
# qt_rectangle = tela.frameGeometry()
# center_point = app.primaryScreen().availableGeometry().center()
# qt_rectangle.moveCenter(center_point)
# tela.move(qt_rectangle.topLeft())
# icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
# icon_login = QIcon(f"{hg.c_imagem}\\login.png")
#
# if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
# else:
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")
#
# pixmap_redimensionado = imagem.scaled(180, 180)  # redimensiona a imagem para 100x100
# tela.lb_imagem.setPixmap(pixmap_redimensionado)
#
# logohti = QPixmap(f"{hg.c_imagem}\\logoHTI.png")
# pixmap_redimensionado = logohti.scaled(150, 150)  # redimensiona a imagem para 100x100
# tela.logohti.setStyleSheet(
#     "background-color: rgb(190, 216, 255);border-width: 0px;border-radius: 0px;"
# )
# tela.logohti.setPixmap(pixmap_redimensionado)
#
# lbl_nome_cliente = tela.findChild(QtWidgets.QLabel, "versao")
# lbl_nome_cliente.setText(f"Versao: {hg.VERSAO}")
# print('inicio')
# conexao_banco()
#
#
# def on_close_event(event):
#     tela.close()
#     event.accept()
#     tela.closeEvent = on_close_event
#
#
# def verificar_senha():
#     index = tela.comboBox.currentIndex()
#     mop = tela.comboBox.itemText(index)
#     mcod_op = mop[0:3]
#     entry_senha_editado = str(tela.inp_senha.text().upper().strip())
#     hg.conexao_cursor.execute(
#         f"SELECT * FROM insopera WHERE scod_op = '{mcod_op}' "
#         f"and plug = '{entry_senha_editado}'"
#     )
#     # Recupere o resultado
#     arq_senha = hg.conexao_cursor.fetchone()
#     hg.conexao_bd.commit()
#     if arq_senha is not None:
#         hg.geral_cod_usuario = arq_senha[0]
#         hg.geral_nivel_usuario = arq_senha[12]
#         tela.close()
#         criar_menu()
#     else:
#         QMessageBox.warning(tela, "Erro de login", "SENHA INCORRETA!")
#         tela.inp_senha.clear()
#         tela.inp_senha.setFocus()
#
#
# def fecha_tela():
#     tela.close()
#     tela.closeEvent = on_close_event
#     hg.conexao_cursor.close()
#     hg.conexao_bd.close()
#     app.quit()
#
#
# def dados_login():
#     print('1')
#     if hg.mtipo_temrinal == "S":
#         criar_tabelas()
#
#     hg.conexao_cursor.execute(f"SELECT scod_op,snome FROM insopera")
#     arq_insopera = hg.conexao_cursor.fetchall()
#     hg.conexao_bd.commit()
#
#     for ret_insopera in arq_insopera:
#         item = f"{ret_insopera[0]} - {ret_insopera[1]}".strip("(),")
#         tela.comboBox.addItem(item)
#     tela.inp_senha.setReadOnly(False)
#     tela.inp_senha.returnPressed.connect(verificar_senha)
#     tela.bt_sair.setIcon(icon_sair)
#     tela.bt_login.setIcon(icon_login)
#
#     tela.bt_login.clicked.connect(verificar_senha)
#     tela.bt_sair.clicked.connect(fecha_tela)
#     print('2')
#     tela.show()
#     app.exec()
#
#
# if __name__ == "__main__":
#     dados_login()
#     tela.close()
#     hg.conexao_cursor.close()
#     hg.conexao_bd.close()
#     app.quit()
