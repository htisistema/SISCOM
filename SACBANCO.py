# BANCO

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup
import os
import hti_global as hg

titulo = 'BANCOS CADASTRADAS'
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_banco.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
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


tela.setWindowTitle(titulo)
# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")


def on_close_event(event):
    # Esta função será chamada quando o usuário clicar no botão de fechar a janela
    # print("Fechando a janela...")
    tela.close()
    event.accept()


tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()


# Define a função para ajustar as colunas da tabela
def ajustar_colunas_tabela(tabela):
    header = tabela.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def f_incl_banco():
    from SACBANCO1 import inclusao_banco
    inclusao_banco()
    listar_banco()


def chama_alteracao(mcod_cli):
    from SACBANCO2 import alteracao_banco
    alteracao_banco(mcod_cli)
    listar_banco()


def editar_item(row):
    item = tela.tableWidget.item(row, 0)
    tela.tableWidget.itemDoubleClicked.disconnect()
    print(item.text())
    if tela.rb_alteracao.isChecked():
        chama_alteracao(item.text())
        pass
    else:
        # chama_consulta(item.text())
        pass

    tela.tableWidget.itemDoubleClicked.connect(lambda item1: editar_item(item1.row()))
    return


def listar_banco():
    hg.conexao_cursor.execute(f"SELECT cod_banco, num_banco, nome_banco, agencia, dv_ag, c_c, dv_cc, "
                                      f"dig_ag_cc, modalidade, n_conv, cod_cedente, carteira, cod_trans, diasprot, "
                                      f"REPLACE(CAST(despesa AS DECIMAL(18,2)), '.', ','), local_pg  FROM sacbanco "
                                      f"order BY cod_banco")

    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tela.tableWidget.setRowCount(len(dados_lidos))
    tela.tableWidget.setColumnCount(16)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            item = QtWidgets.QTableWidgetItem(valor)
            tela.tableWidget.setItem(i, j, item)
            # print(item.text())
    ajustar_colunas_tabela(tela.tableWidget)

    rb_tipo_group = QButtonGroup()
    rb_tipo_group.addButton(tela.rb_alteracao, id=1)
    rb_tipo_group.addButton(tela.rb_exclusao, id=2)
    tela.rb_alteracao.setChecked(True)

    tela.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tela.tableWidget.itemDoubleClicked.connect(lambda item1: editar_item(item1.row()))
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_inclusao.clicked.connect(f_incl_banco)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_inclusao.setIcon(icon_incluir)

    tela.show()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_banco()
    app.exec()
    hg.conexao_bd.close()
