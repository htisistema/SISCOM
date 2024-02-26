# PRINCIPAL

import os
import socket
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QMessageBox
from hti_funcoes import criar_tabelas
import hti_global as hg

# from pyshortcuts import make_shortcut
#
# CRIAR ATALHO
# # Caminho do arquivo executável ou script
# caminho_sistema = '/caminho/do/seu/sistema'
#
# # Caminho da imagem que será usada como ícone
# caminho_imagem = '/caminho/do/seu/arquivo/imagem.jpg'
#
# # Caminho e nome do atalho
# caminho_atalho = '/caminho/do/seu/atalho.lnk'
#
# # Cria o atalho
# make_shortcut(caminho_sistema, caminho_atalho, icon=caminho_imagem)


# VERSAO = 'v23.04.13'
# SIT_TIP = 'SISCOM'
# SISTEMA = '.: SISCOM :. Sistema Automacao Comercial'
# HTISISTEMA = '.: HTI Sistemas Ltda :.'
# CNPJ_HTI = '24494200000106'
# INSC_MUNCI = '066728339'
# RAZAO_HTI = 'M. EDUARDA B. B. CINTRA'
# END_HTI = 'Rua Cicero Monteiro'
# MNUM_HTI = '1040'
# COMP_HTI = ''
# BAIRRO_HTI = 'Centro'
# CIDADE_HTI = 'Tacaimbo'
# UF_HTI = 'PE'
# CEP_HTI = '55140000'
# FONE_HTI = '993127894'

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file = os.path.basename(__file__)
nome_computador = socket.gethostname()
endereco_ip = socket.gethostbyname(nome_computador)

# print(ip_address)

# logging.basicConfig(filename='siscom.log', level=logging.INFO)
# logging.error('Starting my app')

# Crie a janela
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\siscom.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
tela.setWindowIcon(icon)
tela.setWindowTitle(f'LOGIN         {hg.SISTEMA}  Versao: {hg.VERSAO}')
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_login = QIcon(f"{hg.c_imagem}\\login.png")

if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(180, 180)  # redimensiona a imagem para 100x100
tela.lb_imagem.setPixmap(pixmap_redimensionado)

logohti = QPixmap(f"{hg.c_imagem}\\logoHTI.png")
pixmap_redimensionado = logohti.scaled(150, 150)  # redimensiona a imagem para 100x100
tela.logohti.setStyleSheet("background-color: rgb(190, 216, 255);border-width: 0px;border-radius: 0px;")
tela.logohti.setPixmap(pixmap_redimensionado)

lbl_nome_cliente = tela.findChild(QtWidgets.QLabel, "versao")
lbl_nome_cliente.setText(f'Versao: {hg.VERSAO}')

# tela.statusBar.showMessage("Mensagem de status")

# # setar COR DARK
# app.setStyleSheet("""
#     QWidget {
#         background-color: #1E1E1E;
#         color: #F8F8F8;
#     }
#     QLabel#my_label {
#         background-color: #778899;
#         padding: 10px;
#         font-size: 24px;
#     }
# """)


def on_close_event(event):
    tela.close()
    event.accept()


tela.closeEvent = on_close_event

# mconf_nivel = '26'
# letra1 = mconf_nivel[0]
# letra2 = mconf_nivel[1]
# presente1 = letra1 in '135'
# presente2 = letra2 in '135'
# print(presente1)
# print(presente2)
# print(letra1)
# print(letra2)
# if not presente1 and not presente2:
#     print('falso')
# else:
#     print('Verdadeiro')


def verificar_senha():
    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    mcod_op = mop[0:3]
    entry_senha_editado = str(tela.inp_senha.text().upper().strip())
    hg.conexao_cursor.execute(f"SELECT * FROM insopera WHERE scod_op = '{mcod_op}' "
                              f"and plug = '{entry_senha_editado}'")
    # Recupere o resultado
    arq_senha = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_senha is not None:
        hg.geral_cod_usuario = arq_senha[0]
        hg.geral_nivel_usuario = arq_senha[12]
        from menu import criar_menu
        tela.close()
        criar_menu()
    else:
        QMessageBox.warning(tela, "Erro de login", "SENHA INCORRETA!")
        tela.inp_senha.clear()
        tela.inp_senha.setFocus()


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    hg.conexao_cursor.close()
    hg.conexao_bd.close()
    app.quit()


def dados_login():
    # hg.conexao_cursor.execute("SELECT * FROM sacsetup")
    # # Recupere o resultado
    # m_set = hg.conexao_cursor.fetchall()
    # hg.conexao_bd.commit()

    if hg.mtipo_temrinal == "S":
        criar_tabelas()

    # PEGAR O ULTIMO NUMERO DOS CLIENTE E ACRESCENTA 1
    hg.conexao_cursor.execute(f"SELECT scod_op,snome FROM insopera")
    arq_insopera = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()

    for ret_insopera in arq_insopera:
        item = f'{ret_insopera[0]} - {ret_insopera[1]}'.strip('(),')
        tela.comboBox.addItem(item)
    tela.inp_senha.setReadOnly(False)
    tela.inp_senha.returnPressed.connect(verificar_senha)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_login.setIcon(icon_login)

    tela.bt_login.clicked.connect(verificar_senha)
    tela.bt_sair.clicked.connect(fecha_tela)

    tela.show()
    app.exec()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco, verificar_conexao
    conexao_banco()
    verificar_conexao()
    dados_login()
    # Feche a conexão
    tela.close()
    hg.conexao_cursor.close()
    hg.conexao_bd.close()
    app.quit()
