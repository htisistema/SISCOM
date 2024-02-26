# PRINCIPAL

import os
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox
# from icecream import ic
import socket
from hti_funcoes import criar_tabelas
import hti_global as hg

from hti_funcoes import conexao_banco, verificar_conexao
conexao_banco()
verificar_conexao()

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


VERSAO = "v23.12.13"
SIT_TIP = "SISHOST"
SISTEMA = ".: SISHOST :. Sistema Automacao Hoteis e Restaurante"
HTISISTEMA = ".: HTI Sistemas Ltda :."
CNPJ_HTI = "24494200000106"
INSC_MUNCI = "066728339"
RAZAO_HTI = "M. EDUARDA B. B. CINTRA"
END_HTI = "Rua Cicero Monteiro"
MNUM_HTI = "1040"
COMP_HTI = ""
BAIRRO_HTI = "Centro"
CIDADE_HTI = "Tacaimbo"
UF_HTI = "PE"
CEP_HTI = "55140000"
FONE_HTI = "991269631"

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
tela = uic.loadUi(f"{hg.c_ui}\\sishost.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
tela.setWindowIcon(icon)
tela.setWindowTitle(f"LOGIN         {SISTEMA}  Versao: {VERSAO}")
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
pixmap_redimensionado = logohti.scaled(120, 120)  # redimensiona a imagem para 100x100
tela.logohti.setPixmap(pixmap_redimensionado)

lbl_nome_cliente = tela.findChild(QtWidgets.QLabel, "versao")
lbl_nome_cliente.setText(f"Versao: {VERSAO}")

if hg.mtipo_temrinal == "S":
    criar_tabelas()

# PEGAR O ULTIMO NUMERO DOS CLIENTE E ACRESCENTA 1
hg.conexao_cursor.execute(f"SELECT scod_op,snome FROM insopera")
arq_insopera = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_insopera in arq_insopera:
    item = f"{ret_insopera[0]} - {ret_insopera[1]}".strip("(),")
    tela.comboBox.addItem(item)


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


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    hg.conexao_cursor.close()
    hg.conexao_bd.close()
    app.quit()


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


# def verificar_senha():
#     msenha = tela.inp_senha.text()
#     if len(msenha) == 0:
#         QMessageBox.warning(tela, "Erro de login", "SENHA INCORRETA!")
#         tela.inp_senha.clear()
#         tela.inp_senha.setFocus()
#         dados_login()
#     else:
#         tela.inp_senha.returnPressed.disconnect()
#         index = tela.comboBox.currentIndex()
#         mop = tela.comboBox.itemText(index)
#         mcod_op = mop[0:3]
#         entry_senha_editado = str(tela.inp_senha.text().upper().strip())
#         hg.conexao_cursor.execute(
#             f"SELECT * FROM insopera WHERE scod_op = '{mcod_op}' "
#             f"and plug = '{entry_senha_editado}'"
#         )
#         # Recupere o resultado
#         arq_senha = hg.conexao_cursor.fetchone()
#         ic(arq_senha)
#         hg.conexao_bd.commit()
#         if arq_senha is not None:
#             hg.geral_cod_usuario = arq_senha[0]
#             hg.geral_nivel_usuario = arq_senha[12]
#             from MENU import criar_menu
#             tela.close()
#             criar_menu()
#         else:
#             ic()
#             QMessageBox.warning(tela, "Erro de login", "SENHA INCORRETA!")
#             tela.inp_senha.clear()
#             tela.inp_senha.setFocus()
#             dados_login()

def verificar_senha():
    msenha = tela.inp_senha.text()
    tela.inp_senha.returnPressed.disconnect()
    tela.bt_login.clicked.disconnect()
    # Verifica se a senha está vazia
    if len(msenha) == 0:
        QMessageBox.warning(tela, "Erro de login", "SENHA EM BRANCO!")
        tela.inp_senha.clear()
        tela.inp_senha.setFocus()
        dados_login()
        return

    # Converte a senha para uppercase e remove espaços no início e no final
    entry_senha_editado = str(tela.inp_senha.text().upper().strip())

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    mcod_op = mop[0:3]

    hg.conexao_cursor.execute(
        f"SELECT * FROM insopera WHERE scod_op = '{mcod_op}' "
        f"and plug = '{entry_senha_editado}'"
    )

    # Recupere o resultado
    arq_senha = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()

    if arq_senha is not None:
        # Se a senha estiver correta, continue o fluxo do programa
        hg.geral_cod_usuario = arq_senha[0]
        hg.geral_nivel_usuario = arq_senha[12]
        from MENU import criar_menu
        tela.close()
        criar_menu()
    else:
        # Se a senha estiver incorreta, exiba a mensagem
        QMessageBox.warning(tela, "Erro de login", "SENHA NAO CONFERE !")
        tela.inp_senha.clear()
        tela.inp_senha.setFocus()
        dados_login()


def dados_login():
    msenha = tela.inp_senha.text()
    if len(msenha) == 0:
        tela.inp_senha.setFocus()

    tela.inp_senha.setReadOnly(False)
    tela.inp_senha.returnPressed.connect(verificar_senha)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_login.setIcon(icon_login)

    tela.bt_login.clicked.connect(verificar_senha)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.show()
    app.exec()


if __name__ == "__main__":
    # from hti_funcoes import conexao_banco, verificar_conexao
    # conexao_banco()
    # verificar_conexao()
    dados_login()
    # Feche a conexão
    tela.close()
    hg.conexao_cursor.close()
    hg.conexao_bd.close()
    app.quit()
