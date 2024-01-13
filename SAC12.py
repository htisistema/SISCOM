# LISTA DE TRANSPORTADORA

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QTableWidgetItem, QAbstractItemView
import os
import hti_global as hg

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_transportadora.ui")
tela.setWindowTitle('TRANSPORTADORA CADASTRADO')
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
icon_cancelar = QIcon(f"{hg.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hg.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
if hg.mtp_tela == 'G':
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)


tabela = tela.tableWidget

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar = QtWidgets.QStatusBar()
tela.setStatusBar(tela.statusBar)
tela.statusBar.showMessage(f"<< {nome_file} >>")


def on_close_event(event):
    # Esta função será chamada quando o usuário clicar no botão de fechar a janela
    # print("Fechando a janela...")
    tela.close()
    event.accept()
    app.quit()
    tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    app.quit()
    return


# Define a função para ajustar as colunas da tabela
def ajustar_colunas_tabela(tabela1):
    header = tabela1.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def chama_alteracao(mcod_cli):
    from SAC121 import alteracao_transportadora
    alteracao_transportadora(mcod_cli)
    print('ok')
    listar_transportadora()


def editar_item(row):
    item = tabela.item(row, 0)
    print(item.text())
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        chama_alteracao(item.text())
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda item1: editar_item(item1.row()))
    return


def f_incl_transportadora():
    from SAC120 import inclusao_transportadora
    inclusao_transportadora()
    listar_transportadora()


def listar_transportadora():
    hg.conexao_cursor.execute(f"SELECT CAST(cod_tran as char(5)),COALESCE(razao, ' '),"
                                      f"COALESCE(cgc, ' '),"
                                      f"COALESCE(cpf, ' '), "
                                      f"tel1, cidade,"
                                      f"uf,  "
                                      f"placa,  "
                                      f"uf_placa,  "
                                      f"antt  "
                                      f"FROM sactran")
    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tabela.setRowCount(len(dados_lidos))
    tabela.setColumnCount(10)
    tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            item = QTableWidgetItem(valor)
            tabela.setItem(i, j, item)
    ajustar_colunas_tabela(tabela)

    tabela.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tabela.itemDoubleClicked.connect(lambda item2: editar_item(item2.row()))
    rb_tipo_group = QButtonGroup()
    rb_tipo_group.addButton(tela.rb_alteracao, id=1)
    rb_tipo_group.addButton(tela.rb_exclusao, id=1)
    tela.rb_alteracao.setChecked(True)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_inclusao.clicked.connect(f_incl_transportadora)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_inclusao.setIcon(icon_incluir)

    tela.show()
    app.exec()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_transportadora()
    hg.conexao_bd.close()
    tela.close()
    app.quit()
