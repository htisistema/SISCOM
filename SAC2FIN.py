# ALIQUOTA FINANCIAMENTO

from PyQt6 import QtCore
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup
import os
import hti_global

app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\lista_aliquota_fin.ui")
tela.setWindowTitle('ALIQUOTAS CADASTRADAS')
icon = QIcon(f"{hti_global.c_imagem}\\htiico.jpg")
icon_cancelar = QIcon(f"{hti_global.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hti_global.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hti_global.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hti_global.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
if hti_global.mtp_tela == 'G':
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)


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
    # header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    # header.setStretchLastSection(True)
    header.setStretchLastSection(False)


def f_incl_aliquota(mcod_fin):
    from SAC2FIN1 import inclusao_aliquota
    inclusao_aliquota(mcod_fin)
    return


def chama_alteracao(mcod_fin, mtipo_fin):
    from SAC2FIN2 import alteracao_aliquota
    alteracao_aliquota(mcod_fin, mtipo_fin)
    return


def chama_exclusao(mcod_fin, mtipo_fin):
    # from SAC2FIN2 import exclusao_aliquota
    # exclusao_aliquota(mcod_fin, mtipo_fin, mtipo_cons)
    return


def editar_item(row):
    rb_tipo_consulta = None
    item = tela.tableWidget.item(row, 0)
    item2 = tela.tableWidget.item(row, 5)
    mitem = item.text()
    mitem2 = item2.text()
    mitem2 = mitem2.replace('-', '').zfill(3)

    if item.isSelected():
        tela.tableWidget.itemDoubleClicked.disconnect()
        # print("Duplo clique!")
    else:
        tela.tableWidget.itemDoubleClicked.disconnect()
        # print("Clique simples.")

    # print(item.text())
    if tela.rb_inclusao.isChecked():
        rb_tipo_consulta = 'I'

    if tela.rb_alteracao.isChecked():
        rb_tipo_consulta = 'A'

    if tela.rb_exclusao.isChecked():
        rb_tipo_consulta = 'E'

    if rb_tipo_consulta == 'A':
        chama_alteracao(mitem, mitem2)
        return
    elif rb_tipo_consulta == "E":
        chama_exclusao(mitem, mitem2)
        return
    elif rb_tipo_consulta == "I":
        mitem = item.text()
        f_incl_aliquota(mitem)
        return

    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    return


def listar_aliquota():
    hti_global.conexao_cursor.execute(f"SELECT CAST(cod_fin as char(5)), "
                                      f"CAST(desc_fin as char(25)), "
                                      f"REPLACE(CAST(taxa_fin AS DECIMAL(18,2)), '.', ','), "
                                      f"REPLACE(CAST(taxa_adm AS DECIMAL(18,2)), '.', ','), "
                                      f"iif(cobra_fin = 'S','Sim','Nao'), "
                                      f"substring(tipo_fin from 1 for 1) || '-' || substring(tipo_fin from 2 for 2), "
                                      f"REPLACE(CAST(aliq_fin AS DECIMAL(18,2)), '.', ',') "
                                      f"FROM sacfin ORDER BY cod_fin")

    dados_lidos = hti_global.conexao_cursor.fetchall()
    hti_global.conexao_bd.commit()
    tela.tableWidget.setRowCount(len(dados_lidos))
    tela.tableWidget.setColumnCount(7)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            item = QtWidgets.QTableWidgetItem(valor)
            tela.tableWidget.setItem(i, j, item)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

    ajustar_colunas_tabela(tela.tableWidget)

    rb_tipo_group = QButtonGroup()
    rb_tipo_group.addButton(tela.rb_inclusao, id=1)
    rb_tipo_group.addButton(tela.rb_alteracao, id=1)
    rb_tipo_group.addButton(tela.rb_exclusao, id=1)
    tela.rb_inclusao.setChecked(True)
    tela.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))

    # tela.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    # tela.bt_incl_aliquota.clicked.connect(f_incl_aliquota)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)

    tela.show()
    app.exec()


tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_aliquota()
    hti_global.conexao_bd.close()
